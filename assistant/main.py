from time import sleep

from assistant.deepseek_input import DeepseekInput
from assistant.server import listen_for_data


while True:
    with listen_for_data() as server:
        data = server.wait_for_data()
        if data is not None:
            with DeepseekInput() as input:
                if data.new_chat:
                    input.create_new_chat()
                    if data.expert_mode:
                        _ = input.expert_mode()
                else:
                    input._switch_to_desktop(2)

                _ = input.message_field()
                input.submit_prompt(data.get_query())
                _ = input.submit_message_field()

                sleeped = 0
                while sleeped < 120:
                    copied = input.copy()
                    if copied is not None and len(copied) > 0:
                        server.answer(copied)
                        break
                    sleep(1)
                    sleeped += 1
