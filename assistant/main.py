from assistant.deepseek_input import DeepseekInput


with DeepseekInput() as input:
    input._switch_to_desktop(2)
    print(input.message_field())
    input.submit_prompt("type hello world please")
    print(input.submit_message_field())
