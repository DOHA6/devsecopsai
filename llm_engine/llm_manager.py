"""
LLM Provider Manager
Handles different LLM providers (OpenAI, Anthropic, Ollama, DeepSeek, Hugging Face)
Optimized for speed with caching and parallel processing
"""

import os
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Optional
from loguru import logger
from abc import ABC, abstractmethod
from functools import lru_cache


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
        """Generate using OpenAI API with speed optimizations"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert cybersecurity policy writer. Be concise."},
                    {"role": "user", "content": prompt}
                ],
                temperature=kwargs.get('temperature', 0.3),
                max_tokens=kwargs.get('max_tokens', 800),  # Reduced for speed
                stream=False,  # Disable streaming for faster completion
                timeout=30  # 30 second timeout
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
        """Generate using Anthropic API with speed optimizations"""
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=kwargs.get('max_tokens', 800),  # Reduced for speed
                temperature=kwargs.get('temperature', 0.3),
                messages=[
                    {"role": "user", "content": prompt}
                ],
                timeout=30  # 30 second timeout
            )
            return message.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise


class OllamaProvider(LLMProvider):
    """Ollama local LLM provider (optimized for speed)"""
    
    def __init__(self, model: str = "qwen2.5:1.5b", host: str = "http://localhost:11434"):
        try:
            import ollama
        except ImportError:
            raise ImportError("Ollama package not installed. Run: pip install ollama")
        
        self.model = model
        self.host = host
        self.client = ollama.Client(host=self.host, timeout=120.0)
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate using Ollama with optimized settings for speed"""
        import threading
        
        try:
            # Ultra-optimized settings for fastest response times
            options = {
                'temperature': kwargs.get('temperature', 0.2),  # Balanced for accuracy
                'num_predict': min(kwargs.get('max_tokens', 200), 250),  # Cap at 250
                'top_p': 0.9,
                'top_k': 30,  # Balanced for quality
                'repeat_penalty': 1.1,
                'num_ctx': 512,  # Small context window for speed
                # Speed optimizations
                'num_thread': 4,  # Fixed 4 threads
                'num_batch': 128,  # Larger batches for qwen
            }
            
            logger.debug(f"Generating with Ollama (model: {self.model}, tokens: {options['num_predict']}, threads: {options['num_thread']})")
            
            # Use threading-safe timeout instead of signal
            result = {'response': None, 'error': None}
            
            def generate_with_timeout():
                try:
                    response = self.client.generate(
                        model=self.model,
                        prompt=prompt,
                        options=options,
                        stream=False,  # Disable streaming for faster processing
                        keep_alive='5m'  # Keep model loaded in memory
                    )
                    result['response'] = response
                except Exception as e:
                    result['error'] = e
            
            thread = threading.Thread(target=generate_with_timeout)
            thread.daemon = True
            thread.start()
            thread.join(timeout=90)  # 90 second timeout
            
            if thread.is_alive():
                raise TimeoutError("Ollama request timed out after 90 seconds")
            
            if result['error']:
                raise result['error']
            
            if not result['response'] or 'response' not in result['response']:
                raise ValueError("Invalid response from Ollama")
            
            return result['response']['response']
            
        except TimeoutError as e:
            logger.error(f"Ollama request timed out - check if Ollama is running: {e}")
            raise
        except Exception as e:
            logger.error(f"Ollama generation error: {e}")
            logger.error(f"Model: {self.model}, Host: {self.host}")
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
        """Generate using DeepSeek API with speed optimizations"""
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
                        {"role": "system", "content": "You are an expert cybersecurity policy writer. Be concise."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": kwargs.get('temperature', 0.3),
                    "max_tokens": kwargs.get('max_tokens', 800),  # Reduced for speed
                    "stream": False
                },
                timeout=30  # 30 second timeout
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
    """Manages LLM provider selection and interaction with caching"""
    
    def __init__(self, provider: Optional[str] = None, model: Optional[str] = None, use_cache: bool = True):
        """
        Initialize LLM Manager
        
        Args:
            provider: LLM provider name (openai, anthropic, ollama, deepseek, huggingface)
            model: Specific model to use (overrides defaults)
            use_cache: Enable response caching for identical prompts
        """
        self.provider_name = provider or os.getenv('LLM_PROVIDER', 'openai')
        self.model = model or os.getenv('LLM_MODEL')
        self.use_cache = use_cache and os.getenv('DISABLE_LLM_CACHE', 'false').lower() != 'true'
        
        # Setup cache directory
        self.cache_dir = Path(os.getenv('LLM_CACHE_DIR', './cache/llm'))
        if self.use_cache:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Initializing LLM: {self.provider_name} (cache: {self.use_cache})")
        
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
    
    def _get_cache_key(self, prompt: str, **kwargs) -> str:
        """Generate cache key from prompt and parameters"""
        # Create unique hash from prompt and relevant kwargs
        cache_data = {
            'prompt': prompt,
            'provider': self.provider_name,
            'model': self.model,
            'temperature': kwargs.get('temperature', 0.3),
            'max_tokens': kwargs.get('max_tokens', 512)
        }
        cache_str = json.dumps(cache_data, sort_keys=True)
        return hashlib.sha256(cache_str.encode()).hexdigest()
    
    def _get_cached_response(self, cache_key: str) -> Optional[str]:
        """Retrieve cached response if available"""
        if not self.use_cache:
            return None
        
        cache_file = self.cache_dir / f"{cache_key}.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    cached = json.load(f)
                    logger.debug(f"Cache hit for key: {cache_key[:8]}...")
                    return cached.get('response')
            except Exception as e:
                logger.warning(f"Cache read error: {e}")
        return None
    
    def _save_to_cache(self, cache_key: str, response: str):
        """Save response to cache"""
        if not self.use_cache:
            return
        
        cache_file = self.cache_dir / f"{cache_key}.json"
        try:
            with open(cache_file, 'w') as f:
                json.dump({'response': response, 'timestamp': str(Path(cache_file).stat().st_mtime)}, f)
            logger.debug(f"Cached response for key: {cache_key[:8]}...")
        except Exception as e:
            logger.warning(f"Cache write error: {e}")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text using configured provider with caching"""
        # Check cache first
        cache_key = self._get_cache_key(prompt, **kwargs)
        cached_response = self._get_cached_response(cache_key)
        if cached_response:
            return cached_response
        
        # Generate new response
        response = self.provider.generate(prompt, **kwargs)
        
        # Cache the response
        self._save_to_cache(cache_key, response)
        
        return response
    
    def generate_with_retry(self, prompt: str, max_retries: int = 2, **kwargs) -> str:
        """Generate with automatic retry on failure (reduced retries for speed)"""
        import time
        
        for attempt in range(max_retries):
            try:
                return self.generate(prompt, **kwargs)
            except Exception as e:
                logger.warning(f"Generation attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)  # Reduced backoff time
                else:
                    raise
