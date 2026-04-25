from assistant.deepseek_input import DeepseekInput
from assistant.server import listen_for_data


while True:
    with listen_for_data() as server:
        data = server.wait_for_data()
        if data is not None:
            with DeepseekInput() as input:
                input.create_new_chat()
                _ = input.message_field()
                input.submit_prompt(data)
                _ = input.submit_message_field()

                copied = input.copy()
                if copied is not None:
                    server.answer(copied)
