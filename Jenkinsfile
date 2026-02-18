pipeline {
    agent any

    environment {
        CLUSTER_NAME = "enterprise-cluster"
        IMAGE_NAME = "backend"
        IMAGE_TAG = "${BUILD_NUMBER}"
        KUBECONFIG = "/Users/mananrawat/.kube/config"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                cd services/be
                docker build -t $IMAGE_NAME:$IMAGE_TAG services/backend/
                '''
            }
        }

        stage('Load Image into KIND') {
            steps {
                sh '''
                kind load docker-image $IMAGE_NAME:$IMAGE_TAG --name $CLUSTER_NAME
                '''
            }
        }

        stage('Deploy Based on Branch') {
            steps {
                script {
                    if (env.BRANCH_NAME == 'dev') {
                        sh '''
                        kubectl set image deployment/backend \
                        backend=$IMAGE_NAME:$IMAGE_TAG \
                        -n dev
                        '''
                    }
                    else if (env.BRANCH_NAME == 'test') {
                        sh '''
                        kubectl set image deployment/backend \
                        backend=$IMAGE_NAME:$IMAGE_TAG \
                        -n dev
                        '''
                    }
                    else if (env.BRANCH_NAME == 'main') {
                        sh '''
                        kubectl set image deployment/backend \
                        backend=$IMAGE_NAME:$IMAGE_TAG \
                        -n prod
                        '''
                    }
                }
            }
        }

        stage('Verify Rollout') {
            steps {
                script {
                    if (env.BRANCH_NAME == 'dev') {
                        sh 'kubectl rollout status deployment/backend -n dev'
                    }
                    else if (env.BRANCH_NAME == 'test') {
                        sh 'kubectl rollout status deployment/backend -n dev'
                    }
                    else if (env.BRANCH_NAME == 'main') {
                        sh 'kubectl rollout status deployment/backend -n prod'
                    }
                }
            }
        }
    }
}
