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
            steps {
                // Frontend deployment steps (npm install)
                dir('front_app') {
                    // Ensure npm is installed
                    script {
                        def npmInstalled = sh(script: 'which npm', returnStatus: true)
                        if (npmInstalled != 0) {
                            sh 'sudo apt-get update && sudo apt-get install -y npm'
                        }
                    }

                    // Install npm dependencies
                    sh 'npm install'

                    // Start frontend development server
                    sh 'npm run dev &'
                }
            }
        }
    }
}
