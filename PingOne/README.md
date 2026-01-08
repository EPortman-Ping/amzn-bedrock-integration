# PingOne Integration with Amazon Bedrock AgentCore

This repository contains notebooks demonstrating how to integrate PingOne with Amazon Bedrock AgentCore for various authentication and authorization scenarios.

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

### 1. PingOne for Inbound Auth

**Purpose**: Protect AgentCore Runtime endpoints so only authenticated users can invoke agents. Users authenticate with PingOne, then use the resulting JWT to securely call agents via REST API.

**What you'll learn**:
- Configure PingOne resources, applications, and test users
- Deploy agents to AgentCore Runtime with custom JWT authorization
- Implement the device authorization flow for user authentication
- Invoke agents with Bearer tokens and manage session continuity

**Key Integration Pattern**:
```
User → PingOne (device auth) → JWT → AgentCore Runtime → Agent
```
- Users authenticate with PingOne and receive a JWT
- AgentCore Runtime validates the JWT (issuer, audience, scopes) before processing
- Session IDs enable multi-turn conversations with authenticated users

### 2. PingOne for Outbound Auth

**Purpose**: Enable agents to access external APIs on behalf of authenticated users. Users grant permission via OAuth, and the agent uses delegated tokens to call protected resources.

**What you'll learn**:
- Configure PingOne applications for authorization code flow
- Register PingOne as an OAuth2 credential provider with AgentCore Identity
- Use the `@requires_access_token` decorator for automatic token management
- Build tools that call PingOne APIs on behalf of authenticated users

**Key Integration Pattern**:
```
User → Agent → OAuth2 Flow (PingOne) → Access Token → PingOne API
```
- Agent triggers OAuth authorization when it needs to access user's data
- User authenticates with PingOne and grants permission to the agent
- AgentCore Identity manages token storage and refresh automatically
- Agent calls PingOne userinfo endpoint to retrieve user profile

### 3. PingOne for Gateway Auth

**Purpose**: Secure AgentCore Gateway endpoints with machine-to-machine authentication. Applications authenticate with PingOne using client credentials, then use the resulting JWT to invoke Lambda-backed tools via the MCP interface.

**What you'll learn**:
- Configure PingOne resources and applications for client credentials flow
- Deploy Lambda functions as agent tools with custom schemas
- Create an AgentCore Gateway with custom JWT authorization
- Invoke MCP tools through an authenticated Gateway connection

**Key Integration Pattern**:
```
Application → PingOne (client credentials) → JWT → Gateway → Lambda Tools
```
- Applications authenticate with PingOne using client credentials (no user interaction)
- Gateway validates the JWT (issuer, audience, scopes) before allowing tool invocation
- Lambda functions are exposed as standardized MCP tools for agents to consume

## Support and Documentation

- [PingOne Developer Documentation](https://developer.pingidentity.com/pingone.html/)
- [Amazon Bedrock AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/)
- [OAuth 2.0 and OpenID Connect](https://developer.okta.com/docs/concepts/oauth-openid/)
