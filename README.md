# Upload Videos Periodically From Drive to YouTube
## Installation
- Create virtual environment
```sh
cd ~
python3 -m venv py_env
echo "alias load='source ~/py_env/bin/activate'" >> ~/.bashrc
source ~/.bashrc
```
- Clone repository and install libraries
```sh
cd ~
git clone git@github.com:Alperenlcr/YouTube_Uploader.git
git checkout v0.1.0
load
pip3 install req.txt
```
- Arrange credentials and test
- - Get the credentials of yours from `Google Drive API` and `YouTube Data API`.\
    And modify the json files.
- - Defualt is credentials testing mode in config.py
    ```python
    testing_cred = True
    pause_minutes = 0.01
    ```
- - Testing:
    ```sh
    ~/py_env/bin/python3 ~/YouTube_Uploader/helper.py
    ```
- Rent a server and automate by adding these lines into `crontab -e`.
    ```sh
    SHELL=/bin/bash
    0 16 * * * source ~/py_env/bin/activate && ~/py_env/bin/python3 ~/YouTube_Uploader/helper.py >> ~/log_cron.log 2>&1
    ```
- - Additionally
```sh
echo "cd ~/YouTube_Uploader/ && load" >> ~/.bashrc
```
## Result
Checkout [My YouTube Channel](https://www.youtube.com/@WishYouBestt/videos).
## Related
My TikTok auto uploader [repo](https://github.com/Alperenlcr/TikTok_Uploader).\
Content creation algorithm is private for now but it will be on public anytime.
