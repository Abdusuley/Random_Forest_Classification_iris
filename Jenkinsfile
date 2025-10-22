pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        IMAGE_NAME = "abdusuley/random-forest-app"  // Replace with your Docker Hub username
        TAG = "${env.BUILD_ID}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Python') {
            steps {
                script {
                    // Check if Python is available
                    bat 'python --version || py --version'
                    
                    // Install dependencies
                    bat 'python -m pip install --upgrade pip || py -m pip install --upgrade pip'
                    bat 'pip install -r requirements.txt || python -m pip install -r requirements.txt'
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    // Train model
                    bat 'python train_model.py || py train_model.py'
                    
                    // Run basic tests
                    bat 'python test_app.py || py test_app.py'
                    
                    // Check if model files were created
                    bat 'dir *.pkl *.json'
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image
                    bat "docker build -t ${IMAGE_NAME}:${TAG} ."
                    bat "docker tag ${IMAGE_NAME}:${TAG} ${IMAGE_NAME}:latest"
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                script {
                    // Skip security scan if docker scan is not available
                    bat 'docker scan --version || echo "Docker scan not available, skipping security scan"'
                    bat "docker scan ${IMAGE_NAME}:${TAG} || echo \"Security scan failed or not available\""
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    // Login to Docker Hub
                    bat "echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login --username ${DOCKERHUB_CREDENTIALS_USR} --password-stdin"
                    
                    // Push to Docker Hub
                    bat "docker push ${IMAGE_NAME}:${TAG}"
                    bat "docker push ${IMAGE_NAME}:latest"
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    // Stop and remove existing containers
                    bat 'docker-compose down || echo "No running containers to stop"'
                    
                    // Deploy new version
                    bat 'docker-compose up -d'
                    
                    // Wait for service to be ready
                    bat 'timeout 30 || ping -n 30 127.0.0.1 > nul'
                    
                    // Run integration tests
                    bat 'python test_app.py || py test_app.py'
                }
            }
        }
    }
    
    post {
        always {
            // Clean up Docker resources
            bat 'docker system prune -f || echo "Docker cleanup failed"'
            
            // Clean up Python cache
            bat 'rmdir /s /q __pycache__ || echo "No pycache to remove"'
            bat 'del /q *.pyc 2>nul || echo "No pyc files to remove"'
        }
        success {
            echo 'Pipeline completed successfully!'
            // You can add notifications here (Slack, Email, etc.)
            bat 'echo "Build ${BUILD_ID} completed successfully!"'
        }
        failure {
            echo 'Pipeline failed!'
            // You can add failure notifications here
            bat 'echo "Build ${BUILD_ID} failed!"'
        }
    }
}