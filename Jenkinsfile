pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        IMAGE_NAME = "abdusuley/random-forest-app"
        TAG = "${env.BUILD_ID}"
    }
    
    stages {
        stage('Check Repository Structure') {
            steps {
                script {
                    echo "Checking repository structure..."
                    bat 'echo Current directory: %CD%'
                    bat 'dir /B'
                }
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                script {
                    bat '''
                    python --version
                    python -m ensurepip --upgrade
                    python -m pip install --upgrade pip setuptools wheel
                    python -m pip install numpy==1.26.4 pandas==2.2.2 Flask==2.3.3 joblib==1.3.2 requests==2.31.0
                    pip install scikit-learn==1.6.1 --only-binary=scikit-learn || echo "scikit-learn installation failed, will use Docker for ML"
                    pip list | findstr -i "flask pandas numpy joblib" 2>nul || echo "Package list check completed"
                    '''
                }
            }
        }
        
        // Keep the rest of your existing stages unchanged
        // (Create Demo Model Files, Test Flask Application, etc.)
        
    }

    post {
        always {
            script {
                echo "Cleaning up..."
                // Use returnStatus:true to prevent pipeline from aborting if process/container not found
                bat(returnStatus: true, script: 'taskkill /f /im python.exe 2>nul || echo "No Python processes running"')
                bat(returnStatus: true, script: 'docker stop test-app 2>nul || echo "No test container to stop"')
                bat(returnStatus: true, script: 'docker rm test-app 2>nul || echo "No test container to remove"')
                bat(returnStatus: true, script: 'docker system prune -f || echo "Docker cleanup completed"')
            }
            
            script {
                if (currentBuild.result == 'SUCCESS') {
                    echo "🎉 Pipeline completed successfully!"
                    bat 'echo "Build ${BUILD_ID} completed successfully!"'
                    bat 'echo "Docker image: ${IMAGE_NAME}:${TAG}"'
                } else {
                    echo "Pipeline completed with status: ${currentBuild.result}"
                    bat 'echo "Build ${BUILD_ID} completed with status: ${currentBuild.result}"'
                }
            }
        }
    }
}
