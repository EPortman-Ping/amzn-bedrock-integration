# PingOne Integration with Amazon Bedrock AgentCore

This repository contains three comprehensive notebooks demonstrating how to integrate PingOne with Amazon Bedrock AgentCore for various authentication and authorization scenarios.

## What is PingOne?

PingOne is a cloud-based identity and access management service that provides secure identity solutions for enterprises, enabling seamless authentication and authorization across applications and services.

### Key Features:
- **Single Sign-On (SSO)** - Users authenticate once to access multiple applications
- **Multi-Factor Authentication (MFA)** - Enhanced security through additional verification methods  
- **Adaptive Authentication** - Risk-based authentication policies based on user behavior and context
- **Universal Directory** - Centralized user management and profile synchronization
- **API Access Management** - OAuth 2.0 and OpenID Connect support for API security

### Integration with AgentCore

PingOne can be used as an identity provider with AgentCore Identity to:
- Authenticate users before they can invoke agents (inbound authentication)
- Authorize agents to access protected resources on behalf of users (outbound authentication)
- Secure AgentCore Gateway endpoints with JWT-based authorization

## Example Notebooks Overview

This learning path includes practical notebooks that demonstrate different integration patterns:

### 1. Step by Step PingOne for Inbound Auth.ipynb

**Purpose**: Shows how to use PingOne for **inbound authentication** to protect AgentCore Runtime agent endpoints, ensuring only authenticated users can invoke agents.

**What you'll learn**:
- Setting up PingOne resource and application configuration
- Building and deploying agents on AgentCore Runtime with PingOne integration
- Protecting AgentCore Runtime endpoints with bearer tokens
- Managing session-based conversations with authenticated users

**Key Integration Pattern**:
- Users must authenticate with PingOne before accessing AgentCore Runtime agents endpoints
- Bearer tokens validate user identity on each request
- Agents remain protected behind authentication layer

### 2. Step by Step PingOne for Outbound Auth.ipynb

TODO

### 3. Step by Step PingOne for Gateway Auth.ipynb

**Purpose:** Demonstrates how to use PingOne to secure **AgentCore Gateway** endpoints with machine-to-machine (M2M) authentication using the client credentials flow.

**What you'll learn**:
- Setting up PingOne resource and application configuration
- Creating Lambda functions as MCP (Model Context Protocol) tools
- Configuring AgentCore Gateway with custom JWT authorization
- Using client credentials flow for service-to-service authentication

**Key Integration Pattern**:
- Applications authenticate using client credentials (no user interaction)
- Gateway validates JWT tokens against PingOne
- Lambda functions exposed as standardized MCP tools

## Support and Documentation

- [PingOne Developer Documentation](https://developer.pingidentity.com/pingone.html/)
- [Amazon Bedrock AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/)
- [OAuth 2.0 and OpenID Connect](https://developer.okta.com/docs/concepts/oauth-openid/)

## Note

PingOne is not an AWS service. Please refer to PingOne documentation for costs and licensing related to PingOne usage.
