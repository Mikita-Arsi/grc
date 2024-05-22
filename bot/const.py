from config import is_deploy

admin_chat_id = -1002097272095
if is_deploy:
    main_chat_id = -1001723650175
    forum_id = 24502
else:
    main_chat_id = -1002091679813
    forum_id = 2
