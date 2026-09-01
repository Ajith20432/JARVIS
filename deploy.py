# deploy.py
import os
import subprocess
import requests
from dotenv import load_dotenv

load_dotenv()

class AutonomousDeployer:
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.repo_name = os.getenv("GITHUB_REPO")
        self.render_deploy_hook = os.getenv("RENDER_DEPLOY_HOOK_URL")

    def git_auto_commit_and_push(self):
        """
        ஜார்விஸ் தனது கோட் மாற்றங்களை தானாகவே git-ல் கமிட் செய்து GitHub-க்கு தள்ளும்
        """
        try:
            print("🤖 J.A.R.V.I.S: Preparing autonomous code synchronization...")
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "Autonomous AI self-update and optimization"], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("✅ J.A.R.V.I.S: Code successfully pushed to remote repository.")
            return True
        except Exception as e:
            print(f"⚠️ Git Push Error: {e}")
            return False

    def trigger_cloud_host(self):
        """
        கிளவுட் சர்வரை (Render / Webhook) ட்ரிகர் செய்து இன்டர்நெட்டில் ஆன்லைனில் பப்ளிஷ் செய்யும்
        """
        if self.render_deploy_hook:
            print("🌐 J.A.R.V.I.S: Triggering cloud self-hosting deployment...")
            try:
                response = requests.post(self.render_deploy_hook)
                if response.status_code == 200:
                    print("🚀 J.A.R.V.I.S: Successfully deployed and live on the internet!")
                    return True
                else:
                    print(f"⚠️ Cloud deployment failed with status code: {response.status_code}")
            except Exception as e:
                print(f"⚠️ Cloud Hook Error: {e}")
        else:
            print("ℹ️ Render deployment hook URL not found in environment variables.")
        return False

    def execute_self_hosting(self):
        """
        முழுமையான ஆட்டோமேட்டிக் டெப்ளாய்மென்ட் செயல்முறை
        """
        if self.git_auto_commit_and_push():
            self.trigger_cloud_host()

if __name__ == "__main__":
    deployer = AutonomousDeployer()
    deployer.execute_self_hosting()