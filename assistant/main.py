from assistant.deepseek_input import DeepseekInput


with DeepseekInput() as input:
    input.create_new_chat()
    input.submit_prompt("Hello World")
