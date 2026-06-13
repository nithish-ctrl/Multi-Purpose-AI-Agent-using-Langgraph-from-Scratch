from langchain_community.chat_models import ChatLlamaCpp

def load_model() : 
    model_path = r"D:\Downloads\Qwen3-4B-Q5_K_M.gguf"
    llm = ChatLlamaCpp(
        model_path = model_path,
        temperature = 0.1,
        streaming = False, 
        max_tokens = 512,
        n_ctx = 4096,
        n_batch = 512,
    #    top_p = 0.9,
        model_kwargs={
            "device" : "cuda",
            "chat_format" : "chatml-function-calling",
            "flash_attn" : True
        },
        verbose=False
    )
    return llm


