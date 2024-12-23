pipeline {
    agent any

    environment {
        ROCKET_CHAT_CHANNEL_URL = 'http://13.235.80.174:3000/hooks/6769320793fa2051167e9dfd/GMcqTJLCdZGThQrepJHpde9WxtMFyN2n8e24pM76vwmB2KNp' // Replace with your Rocket.Chat incoming webhook URL
        ROCKET_CHAT_TOKEN = '6769320793fa2051167e9dfd/GMcqTJLCdZGThQrepJHpde9WxtMFyN2n8e24pM76vwmB2KNp' // Your Rocket.Chat token for authentication
        GIT_REPO_URL = 'https://github.com/jawahar1098/thunderbolt.git'
    }

    stages {
        stage('Clone repository') {
            steps {
                git GIT_REPO_URL
                script {
                    def gitCommit = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    rocketChatSend(message: "Git repository cloned. Commit: ${gitCommit}")
                }
            }
        }

        stage('Backend Deployment on Node-1') {
            agent {
                label 'Node-1' // Replace with your Node-1 label
            }
            steps {
                dir('backend') {
                    script {
                        def dockerInstalled = sh(script: 'which docker', returnStatus: true)
                        if (dockerInstalled != 0) {
                            sh 'sudo apt-get update && sudo apt-get install -y docker.io'
                        }
                        
                        def networkExists = sh(script: 'sudo docker network ls --filter name=maze --format "{{.Name}}"', returnStdout: true).trim()
                        if (!networkExists) {
                            sh 'sudo docker network create maze'
                        }

                        def mongoImageExists = sh(script: 'sudo docker images -q mongo', returnStdout: true).trim()
                        if (!mongoImageExists) {
                            sh 'sudo docker pull mongo'
                        }

                        def mongoContainerExists = sh(script: 'sudo docker ps -a --filter name=mymongo --format "{{.Names}}"', returnStdout: true).trim()
                        if (!mongoContainerExists) {
                            sh 'sudo docker run -d --name mymongo --network maze -p 27017:27017 mongo'
                        }
                    }

                    sh '''
                        sudo docker build -t mazebackend .
                        sudo docker run -d -p 5006:5006 --name mazeback --network maze mazebackend 
                    '''

                    script {
                        try {
                            sh 'sudo docker ps'
                            rocketChatSend(message: "Backend deployment successful on Node-1")
                        } catch (Exception e) {
                            rocketChatSend(message: "Backend deployment failed on Node-1: ${e}")
                            throw e
                        }
                    }
                }
            }
        }

        stage('Frontend Deployment on Node-1') {
            agent {
                label 'Node-1' // Replace with your Node-1 label
            }
            steps {
                dir('front_app') {
                    script {
                        sh 'sudo apt-get update'
                        sh 'sudo docker build -t mazefrontend .'
                    }

                    sh 'sudo docker run -d -p 3001:3001 --name mazefront --network maze mazefrontend'

                    script {
                        try {
                            sh 'sudo docker ps'
                            rocketChatSend(message: "Frontend deployment successful on Node-1")
                        } catch (Exception e) {
                            rocketChatSend(message: "Frontend deployment failed on Node-1: ${e}")
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
                rocketChatSend(message: "Deployment finished on Node-1. Server status: ${serverStatus}")
            }
        }
        success {
            rocketChatSend(message: "Deployment successful on Node-1")
        }
        failure {
            rocketChatSend(message: "Deployment failed on Node-1")
        }
    }
}

def rocketChatSend(message) {
    def response = httpRequest(
        url: ROCKET_CHAT_CHANNEL_URL,
        httpMode: 'POST',
        contentType: 'APPLICATION_JSON',
        requestBody: """
        {
            "text": "${message}",
            "token": "${ROCKET_CHAT_TOKEN}"
        }
        """
    )
    echo "Rocket.Chat response: ${response}"
}
