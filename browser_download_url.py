import requests

def get_latest_release(owner, repo):
    url = f"https://api.github.com/Sinnisterly/macro-py/releases/latest"
    response = requests.get(url)
    release_data = response.json()
    download_url = release_data['assets'][0]['browser_download_url']
    return download_url

download_url = get_latest_release('Sinnisterly', 'macro-py')
