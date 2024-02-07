environment = {'dev': 'https://dev-icyte-sparc.integrichain.net/non-sso-login',
               'dev3': 'https://icyte-apps-dev3.integrichain.com/non-sso-login',
               'dev4': 'http://icyte-apps-dev4.integrichain.com/non-sso-login',
               'uat': 'https://uat-icyte-sparc.integrichain.net/non-sso-login',
               'AWSdev': 'https://dev-icyte-sparc.integrichain.net/non-sso-login',
               'qa': 'https://qa-icyte-sparc.integrichain.net/non-sso-login',
               'perfqa':'https://perfqa-icyte-sparc.integrichain.net/non-sso-login',
               'qamasterdatasupport': 'https://qa-icyte-sparc.integrichain.net/masterdata/support',
               'qa2': 'https://qa2-icyte-sparc.integrichain.net/non-sso-login'
               }
def map_environment(env):
    return environment[env]