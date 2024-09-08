import litellm
from openai import OpenAI
import os
from beartype import beartype
from beartype.typing import Dict, List, Optional

from .error_handler import api_calling_error_exponential_backoff

deepseek_client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

@beartype
@api_calling_error_exponential_backoff(retries=5, base_wait_time=1)
def model_prompting(
    llm_model: str,
    messages: List[Dict[str, str]],
    return_num: Optional[int] = 1,
    max_token_num: Optional[int] = 512,
    temperature: Optional[float] = 0.0,
    top_p: Optional[float] = None,
    stream: Optional[bool] = None,
    mode: Optional[str] = None,
) -> List[str]:
    """
    Select model via router in LiteLLM.
    """
    IS_DEEPSEEK = True
    
    if not IS_DEEPSEEK:
        completion = litellm.completion(
            model=llm_model,
            messages=messages,
            max_tokens=max_token_num,
            # for some models, 'n'(The number of chat completion choices ) is not supported.
            n=return_num,
            top_p=top_p,
            temperature=temperature,
            stream=stream,
        )
        content = completion.choices[0].message.content
    else:
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            max_tokens=max_token_num,
            # for some models, 'n'(The number of chat completion choices ) is not supported.
            n=return_num,
            top_p=top_p,
            temperature=temperature,
            stream=stream,
        )
        content = response.choices[0].message.content

    content_l = [content]
    return content_l
