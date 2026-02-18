pipeline {

    agent {
        docker {
            image 'docker:24.0.5'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        CLUSTER_NAME = "enterprise-cluster"
        IMAGE_NAME   = "backend"
        IMAGE_TAG    = "${BUILD_NUMBER}"
        KUBECONFIG   = "/Users/mananrawat/.kube/config"
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
                docker build -t $IMAGE_NAME:$IMAGE_TAG .
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

                    def namespace = ""

                    if (env.BRANCH_NAME == 'dev') {
                        namespace = "dev"
                    }
                    else if (env.BRANCH_NAME == 'test') {
                        namespace = "test"
                    }
                    else if (env.BRANCH_NAME == 'main') {
                        namespace = "prod"
                    }
                    else {
                        error("Branch not allowed for deployment")
                    }

                    sh """
                    kubectl set image deployment/backend \
                    backend=$IMAGE_NAME:$IMAGE_TAG \
                    -n ${namespace}
                    """
                }
            }
        }

        stage('Verify Rollout') {
            steps {
                script {

                    def namespace = ""

                    if (env.BRANCH_NAME == 'dev') {
                        namespace = "dev"
                    }
                    else if (env.BRANCH_NAME == 'test') {
                        namespace = "test"
                    }
                    else if (env.BRANCH_NAME == 'main') {
                        namespace = "prod"
                    }

                    sh """
                    kubectl rollout status deployment/backend -n ${namespace}
                    """
                }
            }
        }
    }
}
