pipeline {
    agent any

    stages {
        stage('Clone repository') {
            steps {
                // Clone your repository
                git 'https://github.com/jawahar1098/thunderbolt.git'
            }
        }

        stage('Backend Deployment on Slave') {
            agent {
                label 'slavenode1' // Replace with your slave node label
            }
            steps {
                // Backend deployment steps
                dir('backend') {
                    // Activate the virtual environment (assuming it's named 'env')
                    sh 'source env/bin/activate'

                    // Start the Python backend application
                    sh 'python wsgi.py &'
                }
            }
        }

        stage('Frontend Deployment on Slave') {
            agent {
                label 'slavenode1' // Replace with your slave node label
            }
            steps {
                // Frontend deployment steps
                dir('front_app') {
                    // Install npm dependencies
                    sh 'npm install'

                    // Start frontend development server
                    sh 'npm run dev &'
                }
            }
        }
    }
}

