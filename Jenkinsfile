pipeline {
    agent any

    stages {
        stage('Clone repository') {
            steps {
                git 'https://github.com/jawahar1098/thunderbolt.git'
            }
        }

        stage('Backend Deployment on Slave') {
            agent {
                label 'slavenode1' // Replace with your slave node label
            }
            steps {
                // Create Python virtual environment and install dependencies
                dir('backend') {
                    // Install Python 3 if not already installed
                    script {
                        def pythonInstalled = sh(script: 'which python3', returnStatus: true)
                        if (pythonInstalled != 0) {
                            sh 'sudo apt-get update && sudo apt-get install -y python3'
                        }
                    }

                    // Create and activate virtual environment
                    sh '''
                        python3 -m venv env
                        . env/bin/activate
                    '''

                    // Install Python dependencies from requirements.txt
                    sh 'pip install -r requirements.txt'

                    // Start the Python backend application
                    sh 'python3 wsgi.py &'
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
                // Frontend deployment steps (npm install and run)
                dir('front_app') {
                    // Reset PATH to include system npm and node
                    script {
                        env.PATH = "/usr/local/bin:$env.PATH"
                    }

                    // Ensure npm is installed (assuming it's not in the virtual environment)
                    script {
                        def npmInstalled = sh(script: 'which npm', returnStatus: true)
                        if (npmInstalled != 0) {
                            // Install npm if not found
                            // sh 'sudo apt-get update && sudo apt-get install -y npm'
                        }
                    }

                    // Install npm dependencies
                    sh 'npm install'

                    // Start frontend development server using specified Node.js version
                    script {
                    sh 'npm run dev &'
                    }
                }
            }
        }

    }
}
