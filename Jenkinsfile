pipeline {
  agent any
  stages {
    stage('检出') {
      steps {
        checkout([$class: 'GitSCM',
        branches: [[name: GIT_BUILD_REF]],
        userRemoteConfigs: [[
          url: GIT_REPO_URL,
          credentialsId: CREDENTIALS_ID
        ]]])
      }
    }
    stage('构建编译镜像') {
          steps {
            script {
              docker.withRegistry("https://${CODING_DOCKER_REG_HOST}", "${CODING_ARTIFACTS_CREDENTIALS_ID}") {
                sh "docker build -t ${CODING_DOCKER_IMAGE_NAME}-builder:latest --build-arg builder_image_tag=${CODING_BUILDER_IMAGE_DEFAULT_TAG} -f Dockerfile_gradle ${DOCKER_BUILD_CONTEXT}"
                docker.image("${CODING_DOCKER_IMAGE_NAME}-builder:latest").push()
              }
            }
          }
        }
    stage('构建镜像') {
      steps {
        script {
          docker.withRegistry("https://${CODING_DOCKER_REG_HOST}", "${CODING_ARTIFACTS_CREDENTIALS_ID}") {
            sh "docker build -t ${CODING_DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_VERSION} -f ${DOCKERFILE_PATH} ${DOCKER_BUILD_CONTEXT}"
          }
        }

      }
    }
    stage('推送到制品库') {
      steps {
        script {
          docker.withRegistry("https://${CODING_DOCKER_REG_HOST}", "${CODING_ARTIFACTS_CREDENTIALS_ID}") {
            docker.image("${CODING_DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_VERSION}").push()
          }
        }

      }
    }
  }
  environment {
    DOCKER_BUILD_CONTEXT = '.'
    DOCKER_REPO_NAME = 'docker-image'
    DOCKER_IMAGE_NAME = "${CCI_JOB_NAME}"
    DOCKER_IMAGE_VERSION = "${GIT_LOCAL_BRANCH}-${GIT_COMMIT_SHORT}"
    DOCKERFILE_PATH = "installer/Dockerfile"
    CODING_DOCKER_REG_HOST = "${CCI_CURRENT_TEAM}-docker.pkg.${CCI_CURRENT_DOMAIN}"
    CODING_DOCKER_IMAGE_NAME = "${PROJECT_NAME.toLowerCase()}/${DOCKER_REPO_NAME}/${DOCKER_IMAGE_NAME}"
    CODING_BUILDER_IMAGE_DEFAULT_TAG =sh(returnStdout: true, script: 'if [ $CODING_BUILDER_IMAGE_TAG ];then  echo "$CODING_BUILDER_IMAGE_TAG"; else echo "megarobo-biolauto-docker.pkg.coding.net/hephaestus/docker-image/flux-maxkb-builder:latest" ; fi').trim()
  }
}