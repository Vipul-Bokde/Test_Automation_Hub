import os

environment = {'dev': 'https://dev-icyte-sparc.integrichain.net/non-sso-login',
               'dev2': 'http://icyte-apps-dev2.integrichain.com/non-sso-login',
               'dev3': 'https://icyte-apps-dev3.integrichain.com/non-sso-login',
               'dev4': 'http://icyte-apps-dev4.integrichain.com/non-sso-login',
               'qa': 'https://qa-icyte-sparc.integrichain.net/non-sso-login',
               'uat': 'https://uat-icyte-sparc.integrichain.net/non-sso-login',
               'perfqa':'https://perfqa-icyte-sparc.integrichain.net/non-sso-login'
               }


def map_environment():
    try:
        if 'ENV_NAME' in os.environ:
            env = os.environ.get("ENV_NAME", None)
            print(env)

    except Exception as ex:
        print("Missing environment", ex)
        return None
    return environment[env]
