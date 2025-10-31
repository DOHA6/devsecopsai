"""
LLM Provider Manager
Handles different LLM providers (OpenAI, Anthropic, Ollama, DeepSeek, Hugging Face)
"""

import os
from typing import Dict, List, Optional
from loguru import logger
from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from prompt"""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider"""
    
    def __init__(self, model: str = "gpt-4"):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = model
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate using OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert cybersecurity policy writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=kwargs.get('temperature', 0.3),
                max_tokens=kwargs.get('max_tokens', 2000)
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider"""
    
    def __init__(self, model: str = "claude-3-opus-20240229"):
        try:
            from anthropic import Anthropic
        except ImportError:
            raise ImportError("Anthropic package not installed. Run: pip install anthropic")
        
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.model = model
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate using Anthropic API"""
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=kwargs.get('max_tokens', 2000),
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise


class OllamaProvider(LLMProvider):
    """Ollama local LLM provider"""
    
    def __init__(self, model: str = "llama3.3"):
        try:
            import ollama
        except ImportError:
            raise ImportError("Ollama package not installed. Run: pip install ollama")
        
        self.model = model
        self.host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate using Ollama"""
        try:
            import ollama
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'temperature': kwargs.get('temperature', 0.3),
                    'num_predict': kwargs.get('max_tokens', 2000)
                }
            )
            return response['response']
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            raise


class DeepSeekProvider(LLMProvider):
    """DeepSeek R1 provider"""
    
    def __init__(self, model: str = "deepseek-chat"):
        self.model = model
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        self.base_url = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')
        
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable not set")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate using DeepSeek API"""
        import requests
        
        try:
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "You are an expert cybersecurity policy writer."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": kwargs.get('temperature', 0.3),
                    "max_tokens": kwargs.get('max_tokens', 2000)
                }
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            logger.error(f"DeepSeek API error: {e}")
            raise


class HuggingFaceProvider(LLMProvider):
    """Hugging Face Transformers provider"""
    
    def __init__(self, model: str = "meta-llama/Llama-3.3-70B-Instruct"):
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            import torch
        except ImportError:
            raise ImportError("Transformers not installed. Run: pip install transformers torch")
        
        self.model_name = model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Loading model {model} on {self.device}...")
        
        self.tokenizer = AutoTokenizer.from_pretrained(
            model,
            token=os.getenv('HUGGINGFACE_TOKEN')
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            model,
            token=os.getenv('HUGGINGFACE_TOKEN'),
            device_map="auto",
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        )
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate using Hugging Face Transformers"""
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=kwargs.get('max_tokens', 2000),
                temperature=kwargs.get('temperature', 0.3),
                do_sample=True,
                top_p=0.9
            )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Remove the input prompt from response
            return response[len(prompt):].strip()
        except Exception as e:
            logger.error(f"Hugging Face generation error: {e}")
            raise


class LLMManager:
    """Manages LLM provider selection and interaction"""
    
    def __init__(self, provider: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize LLM Manager
        
        Args:
            provider: LLM provider name (openai, anthropic, ollama, deepseek, huggingface)
            model: Specific model to use (overrides defaults)
        """
        self.provider_name = provider or os.getenv('LLM_PROVIDER', 'openai')
        self.model = model or os.getenv('LLM_MODEL')
        
        logger.info(f"Initializing LLM: {self.provider_name}")
        
        self.provider = self._create_provider()
    
    def _create_provider(self) -> LLMProvider:
        """Create appropriate LLM provider"""
        providers = {
            'openai': OpenAIProvider,
            'anthropic': AnthropicProvider,
            'ollama': OllamaProvider,
            'deepseek': DeepSeekProvider,
            'huggingface': HuggingFaceProvider
        }
        
        provider_class = providers.get(self.provider_name.lower())
        if not provider_class:
            raise ValueError(f"Unknown LLM provider: {self.provider_name}")
        
        if self.model:
            return provider_class(model=self.model)
        else:
            return provider_class()
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text using configured provider"""
        return self.provider.generate(prompt, **kwargs)
    
    def generate_with_retry(self, prompt: str, max_retries: int = 3, **kwargs) -> str:
        """Generate with automatic retry on failure"""
        import time
        
        for attempt in range(max_retries):
            try:
                return self.generate(prompt, **kwargs)
            except Exception as e:
                logger.warning(f"Generation attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise
