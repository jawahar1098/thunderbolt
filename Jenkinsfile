```
pipeline {
    agent any

    environment {
        ROCKET_CHAT_CHANNEL_URL = 'http://13.235.80.174:3000/hooks/6769320793fa2051167e9dfd/GMcqTJLCdZGThQrepJHpde9WxtMFyN2n8e24pM76vwmB2KNp'
        ROCKET_CHAT_TOKEN = '6769320793fa2051167e9dfd/GMcqTJLCdZGThQrepJHpde9WxtMFyN2n8e24pM76vwmB2KNp'
        GIT_REPO_URL = 'https://github.com/jawahar1098/thunderbolt.git'
    }

    stages {
        stage('Clone repository') {
            steps {
                git GIT_REPO_URL
                script {
                    def gitCommit = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    rocketChatSend("Git repository cloned. Commit: ${gitCommit}")
                }
            }
        }

        stage('Backend Deployment on Node-1') {
            agent {
                label 'Node-1'
            }
            steps {
                dir('backend') {
                    script {
                        sh '''
                            docker network inspect maze || docker network create maze
                            docker pull mongo || true
                            docker inspect mymongo || docker run -d --name mymongo --network maze -p 27017:27017 mongo
                        '''
                        sh 'docker build -t mazebackend .'
                        sh 'docker run -d -p 5006:5006 --name mazeback --network maze mazebackend'
                    }
                }
                script {
                    rocketChatSend("Backend deployment successful on Node-1")
                }
            }
        }

        stage('Frontend Deployment on Node-1') {
            agent {
                label 'Node-1'
            }
            steps {
                dir('front_app') {
                    script {
                        sh 'docker build -t mazefrontend .'
                        sh 'docker run -d -p 3001:3001 --name mazefront --network maze mazefrontend'
                    }
                }
                script {
                    rocketChatSend("Frontend deployment successful on Node-1")
                }
            }
        }
    }

    post {
        always {
            script {
                try {
                    def serverStatus = sh(script: 'curl -Is http://localhost:8000 | head -n 1', returnStdout: true).trim()
                    rocketChatSend("Deployment finished. Server status: ${serverStatus}")
                } catch (Exception e) {
                    rocketChatSend("Failed to retrieve server status: ${e.message}")
                }
            }
        }
        success {
            rocketChatSend("Deployment successful on Node-1")
        }
        failure {
            rocketChatSend("Deployment failed on Node-1")
        }
    }
}

def rocketChatSend(message) {
    try {
        httpRequest(
            url: "${env.ROCKET_CHAT_CHANNEL_URL}",
            httpMode: 'POST',
            contentType: 'APPLICATION_JSON',
            requestBody: """
            {
                "text": "${message}"
            }
            """
        )
    } catch (Exception e) {
        echo "Failed to send Rocket.Chat message: ${e.message}"
    }
}

```
