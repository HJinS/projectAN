def DEPLOY_TO

pipeline {
    agent any

    parameters {
        string(name:'DB_HOST', defaultValue: 'dbMysql', description: 'db host')
        string(name:'Db_PASSWORD', defaultValue: 'db1234!', description: 'db password')
        string(name:'DB_NAME', defaultValue: 'dbName', description: 'db name')
        string(name:'DB_USER', defaultValue: 'user1234!', description: 'db user')
        string(name:'db_port', defaultValue: '3360', description: 'db port')
        string(name:'SECRET_KEY', defaultValue: 'secret_key', description: 'drf secret key')
        string(name:'GOOGLE_OAUTH2_CLIENT_ID', defaultValue: 'client id', description: 'google social login client id')
        string(name:'GOOGLE_OAUTH2_CLIENT_SECRET', defaultValue: 'client secret', description: 'google social login client secret')
    }

    stages {
        stage('Decide Deploy To') {
            steps{
                script {
                    if (env.BRANCH_NAME == 'master'){
                        DEPLOY_TO = 'prod'
                    } else if (env.BRANCH_NAME == 'develop'){
                        DEPLOY_TO = 'dev'
                    } else if (env.BRANCH_NAME == 'qa'){
                        DEPLOY_TO = 'qa'
                    }
                }
                echo "DEPLOY_TO: ${DEPLOY_TO}"
            }
        }

        stage('Check deploy parameter') {
            steps {
                script {
                    withAWS(region: 'ap-northeast-2', credentials: 'JenkinsUser'){
                        def db_name = sh(script: "aws ssm get-parameters --name /DB_NAME | jq '.Parameters[0].Value'", returnStdout: true).trim()
                        def db_user = sh(script: "aws ssm get-parameters --name /DB_USER | jq '.Parameters[0].Value'", returnStdout: true).trim()
                        def db_password = sh(script: "aws ssm get-parameters --name /DB_PASSWORD | jq '.Parameters[0].Value'", returnStdout: true).trim()
                        def db_host = sh(script: "aws ssm get-parameters --name /DB_HOST | jq '.Parameters[0].Value'", returnStdout: true).trim()
                        def db_port = sh(script: "aws ssm get-parameters --name /DB_PORT | jq '.Parameters[0].Value'", returnStdout: true).trim()
                        def secret_key = sh(script: "aws ssm get-parameters --name /SECRET_KEY | jq '.Parameters[0].Value'", returnStdout: true).trim()
                        def state = sh(script: "aws ssm get-parameters --name /STATE | jq '.Parameters[0].Value'", returnStdout: true).trim()
                        def django_settings_module = sh(script: "aws ssm get-parameters --name /DJANGO_SETTINGS_MODULE | jq '.Parameters[0].Value'", returnStdout: true).trim()
                        def google_oauth2_client_id = sh(script: "aws ssm get-parameters --name /GOOGLE_OAUTH2_CLIENT_ID | jq '.Parameters[0].Value'", returnStdout: true).trim()
                        def google_oauth2_client_secret = sh(script: "aws ssm get-parameters --name /GOOGLE_OAUTH2_CLIENT_SECRET | jq '.Parameters[0].Value'", returnStdout: true).trim()
                    }
                }
            }
        }
    }
}