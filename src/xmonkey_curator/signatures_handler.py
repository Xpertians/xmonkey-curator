import requests
import os
import json
import pkg_resources

class SignatureUpdater:
    @staticmethod
    def load_etags(etags_file):
        if os.path.exists(etags_file):
            with open(etags_file, 'r') as file:
                return json.load(file)
        return {}

    @staticmethod
    def save_etags(etags, etags_file):
        with open(etags_file, 'w') as file:
            json.dump(etags, file)

    @staticmethod
    def fetch_and_update_signatures(repo_owner, repo_name, signatures_path, resource_package, etags_file='etags.json'):
        etags = SignatureUpdater.load_etags(etags_file)

        api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{signatures_path}"
        response = requests.get(api_url)
        files = response.json()

        for file in files:
            if file['name'].endswith('.json'):
                headers = {}
                if file['name'] in etags:
                    headers['If-None-Match'] = etags[file['name']]

                file_response = requests.get(file['download_url'], headers=headers)
                if file_response.status_code == 304:
                    print(f"No update needed for {file['name']}")
                    continue

                etags[file['name']] = file_response.headers.get('ETag')
                file_content = file_response.content

                file_path = pkg_resources.resource_filename(resource_package, f'signatures/{file["name"]}')

                with open(file_path, 'wb') as f:
                    f.write(file_content)
                print(f"Updated {file['name']}")

        SignatureUpdater.save_etags(etags, etags_file)

# Usage example, ensure to replace placeholders appropriately
# SignatureUpdater.fetch_and_update_signatures('yourGitHubUsername', 'yourRepoName', 'path/to/signatures', 'your_package_name')
