def DEPLOY_TO

pipeline {
    agent any

    parameters {
        
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