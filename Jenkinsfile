pipeline {
    agent any

    environment {
        SLACK_CHANNEL = 'jenkins' // Replace with your Slack channel
        SLACK_CREDENTIALS_ID = '8dgg3XNduLJGAkDODdeuZMQN' // The ID of the Jenkins credentials storing the token
        GIT_REPO_URL = 'https://github.com/jawahar1098/thunderbolt.git'
    }

    stages {
        stage('Clone repository') {
            steps {
                git GIT_REPO_URL
                script {
                    def gitCommit = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    slackSend(channel: SLACK_CHANNEL, message: "Git repository cloned. Commit: ${gitCommit}")
                }
            }
        }

        stage('Backend Deployment on Slave') {
            agent {
                label 'slavenode1' // Replace with your slave node label
            }
            steps {
                dir('backend') {
                    script {
                        def pythonInstalled = sh(script: 'which python3', returnStatus: true)
                        if (pythonInstalled != 0) {
                            sh 'sudo apt-get update && sudo apt-get install -y python3'
                        }
                    }

                    sh '''
                        python3 -m venv env
                        . env/bin/activate
                    '''
                    sh 'pip install -r requirements.txt'

                    script {
                        try {
                            sh 'python3 wsgi.py &'
                            slackSend(channel: SLACK_CHANNEL, message: "Backend deployment successful")
                        } catch (Exception e) {
                            slackSend(channel: SLACK_CHANNEL, message: "Backend deployment failed: ${e}")
                            throw e
                        }
                    }
                }
            }
        }

        stage('Frontend Deployment on Slave') {
            agent {
                label 'slavenode1' // Replace with your slave node label
            }
            environment {
                NODE_VERSION = 'v22.5.1' // Replace with your Node.js version
                NODE_PATH = "/home/node1/.nvm/versions/node/v22.5.1/bin"
            }
            steps {
                dir('front_app') {
                    script {
                        env.PATH = "/home/node1/.nvm/versions/node/v22.5.1/bin:$env.PATH"
                        def npmInstalled = sh(script: 'which npm', returnStatus: true)
                        if (npmInstalled != 0) {
                            // Install npm if not found
                            // sh 'sudo apt-get update && sudo apt-get install -y npm'
                        }
                    }

                    sh 'npm install'

                    script {
                        try {
                            sh 'npm run dev &'
                            slackSend(channel: SLACK_CHANNEL, message: "Frontend deployment successful")
                        } catch (Exception e) {
                            slackSend(channel: SLACK_CHANNEL, message: "Frontend deployment failed: ${e}")
                            throw e
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                def serverStatus = sh(script: 'curl -Is http://localhost:8000 | head -n 1', returnStdout: true).trim()
                slackSend(channel: SLACK_CHANNEL, message: "Deployment finished. Server status: ${serverStatus}")
            }
        }
        success {
            slackSend(channel: SLACK_CHANNEL, message: "Deployment successful")
        }
        failure {
            slackSend(channel: SLACK_CHANNEL, message: "Deployment failed")
        }
    }
}
