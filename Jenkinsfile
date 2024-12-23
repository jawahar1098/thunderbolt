pipeline {
    agent any

    environment {
        GIT_REPO_URL = 'https://github.com/jawahar1098/thunderbolt.git' // GitHub repository URL
    }

    stages {
        stage('Install Docker') {
            steps {
                script {
                    def dockerInstalled = sh(script: 'which docker', returnStatus: true)
                    if (dockerInstalled != 0) {
                        echo "Installing Docker..."
                        sh 'sudo apt-get update && sudo apt-get install -y docker.io'
                    } else {
                        echo "Docker is already installed."
                    }
                }
            }
        }

        stage('Clone repository') {
            steps {
                // Clone the repository directly from GitHub without credentials
                git url: GIT_REPO_URL
                script {
                    // Get the short commit hash
                    def gitCommit = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    echo "Git repository cloned. Commit: ${gitCommit}"
                }
            }
        }

        stage('Backend Deployment on Node-1') {
            agent {
                label 'Node-1' // Replace with your actual slave node label
            }
            steps {
                dir('backend') {
                    script {
                        // Docker setup and deployment for the backend
                        echo "Setting up Docker network and MongoDB container..."
                        sh '''
                            docker network inspect maze || docker network create maze
                            docker pull mongo || true
                            docker inspect mymongo || docker run -d --name mymongo --network maze -p 27017:27017 mongo
                        '''
                        echo "Building and running backend Docker container..."
                        sh 'docker build -t mazebackend .'
                        sh 'docker run -d -p 5006:5006 --name mazeback --network maze mazebackend'
                    }
                }
                script {
                    echo "Backend deployment successful on Node-1"
                }
            }
        }

        stage('Frontend Deployment on Node-1') {
            agent {
                label 'Node-1' // Replace with your actual slave node label
            }
            steps {
                dir('front_app') {
                    script {
                        // Docker setup and deployment for the frontend
                        echo "Building and running frontend Docker container..."
                        sh 'docker build -t mazefrontend .'
                        sh 'docker run -d -p 3001:3001 --name mazefront --network maze mazefrontend'
                    }
                }
                script {
                    echo "Frontend deployment successful on Node-1"
                }
            }
        }
    }

    post {
        always {
            script {
                try {
                    // Check server status and print the status
                    def serverStatus = sh(script: 'curl -Is http://localhost:8000 | head -n 1', returnStdout: true).trim()
                    echo "Deployment finished. Server status: ${serverStatus}"
                } catch (Exception e) {
                    echo "Failed to retrieve server status: ${e.message}"
                }
            }
        }
        success {
            echo "Deployment successful on Node-1"
        }
        failure {
            echo "Deployment failed on Node-1"
        }
    }
}
