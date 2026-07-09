# Issue 1 — Implement Environment Configuration

## Description

The relayer should load and validate all required environment variables during application startup. Missing or invalid configuration should fail fast with a clear error message instead of allowing the server to start in a broken state.

## Requirements and Context

* Create a centralized configuration module.
* Load environment variables using `dotenv`.
* Validate required configuration values.
* Fail application startup if required variables are missing.
* Export a typed/configured object for the rest of the application.

Required variables should include:

* `PORT`
* `RPC_URL`
* `NETWORK_PASSPHRASE`
* `CONTRACT_ID`
* `FEE_BUMP_SECRET_KEY`

## Suggested Execution

```text
git checkout -b feat/environment-configuration

Create config module

Load dotenv

Validate required variables

Export configuration object

Update application bootstrap
```

## Example Commit Message

```text
feat: implement centralized environment configuration
```

---

# Issue 2 — Implement Centralized Error Handling

## Description

Introduce a centralized error handling strategy for the Express application to ensure API responses remain consistent and internal errors are not leaked to clients.

## Requirements and Context

* Create a reusable error middleware.
* Return consistent JSON responses.
* Handle unexpected exceptions.
* Hide stack traces in production.
* Standardize HTTP error responses.

Example response:

```json
{
  "success": false,
  "message": "Invalid request",
  "error": "VALIDATION_ERROR"
}
```

## Suggested Execution

```text
git checkout -b feat/error-handler

Create error middleware

Register middleware

Standardize API responses

Handle unexpected exceptions
```

## Example Commit Message

```text
feat: add centralized error handling middleware
```

---

# Issue 3 — Add Request Validation Middleware

## Description

Incoming API requests should be validated before reaching the service layer to prevent malformed payloads from generating invalid Soroban transactions.

## Requirements and Context

* Create reusable validation middleware.
* Validate request body.
* Validate required fields.
* Return descriptive validation errors.
* Keep validation separate from business logic.

The middleware should be reusable across future endpoints.

## Suggested Execution

```text
git checkout -b feat/request-validation

Create validation middleware

Validate request payloads

Return standardized validation errors

Apply middleware to routes
```

## Example Commit Message

```text
feat: add reusable request validation middleware
```

---

# Issue 4 — Implement Health Check Endpoint

## Description

Expose a lightweight endpoint that allows developers and deployment platforms to verify that the relayer service is running correctly.

## Requirements and Context

Create a health endpoint that returns:

* Service status
* Current environment
* Server timestamp
* API version

Example endpoint:

```text
GET /health
```

Example response:

```json
{
  "status": "ok",
  "service": "padipay-relayer-api",
  "version": "0.1.0",
  "timestamp": "..."
}
```

The endpoint should not require authentication.

## Suggested Execution

```text
git checkout -b feat/health-endpoint

Create health route

Register endpoint

Return service metadata

Add unit tests
```

## Example Commit Message

```text
feat: add application health endpoint
```

---

# Issue 5 — Configure Soroban Contract Client

## Description

The Escrow Service requires a reusable Soroban contract client capable of interacting with the deployed PadiPay escrow contract.

This issue establishes the foundation for all subsequent contract invocation work.

## Requirements and Context

* Read the contract ID from configuration.
* Initialize the Stellar SDK client.
* Create a reusable contract client.
* Export the client for use by the Escrow Service.
* Handle invalid contract configuration gracefully.

This issue should only establish the client and should not invoke contract methods yet.

## Suggested Execution

```text
git checkout -b feat/soroban-contract-client

Configure Stellar SDK

Read contract configuration

Initialize contract client

Export reusable client

Add basic tests
```

## Example Commit Message

```text
feat: configure reusable Soroban contract client
```


# Issue 6 — Implement Soroban Transaction Builder

## Description

Implement the core transaction builder responsible for constructing Soroban contract invocation transactions.

This service translates validated API requests into unsigned Soroban transactions that can later be sponsored and submitted to the Stellar network.

## Requirements and Context

* Create a reusable transaction builder.
* Accept contract method name and arguments.
* Construct an unsigned Soroban transaction.
* Return the transaction XDR.
* Keep transaction construction independent of signing.

The transaction builder should become the single entry point for creating contract invocation transactions.

## Suggested Execution

```text
git checkout -b feat/transaction-builder

Create transaction builder

Accept contract method and arguments

Construct unsigned transaction

Return transaction XDR

Add unit tests
```

## Example Commit Message

```text
feat: implement Soroban transaction builder
```

---

# Issue 7 — Implement Create Escrow Contract Invocation

## Description

Add support for constructing the contract invocation used to create a new escrow.

This is the first end-to-end interaction between the relayer and the PadiPay escrow contract.

## Requirements and Context

* Add a dedicated create escrow method.
* Accept the required escrow parameters.
* Build the appropriate contract invocation.
* Return the generated transaction XDR.
* Validate required arguments before transaction construction.

Do not perform transaction signing or submission in this issue.

## Suggested Execution

```text
git checkout -b feat/create-escrow-invocation

Implement create escrow service

Map request payload

Build contract invocation

Return unsigned transaction

Write unit tests
```

## Example Commit Message

```text
feat: implement create escrow contract invocation
```

---

# Issue 8 — Implement Lock Funds Contract Invocation

## Description

Implement support for constructing the contract invocation responsible for locking escrow funds.

This endpoint represents the first funding step in the escrow lifecycle.

## Requirements and Context

* Add lock funds service method.
* Accept escrow identifier.
* Build lock funds invocation.
* Validate required request parameters.
* Return unsigned transaction XDR.

Keep transaction construction reusable.

## Suggested Execution

```text
git checkout -b feat/lock-funds-invocation

Implement lock funds service

Construct invocation

Validate request

Return unsigned transaction

Add tests
```

## Example Commit Message

```text
feat: implement lock funds contract invocation
```

---

# Issue 9 — Implement Release & Refund Contract Invocations

## Description

Implement the remaining happy-path escrow actions by supporting both release and refund contract invocations.

These operations complete the MVP escrow lifecycle.

## Requirements and Context

* Implement release funds invocation.
* Implement refund invocation.
* Validate escrow identifier.
* Return unsigned transaction XDR.
* Keep implementation consistent with existing escrow methods.

Do not implement dispute resolution in this milestone.

## Suggested Execution

```text
git checkout -b feat/release-refund-invocations

Implement release invocation

Implement refund invocation

Validate requests

Return transaction XDR

Write unit tests
```

## Example Commit Message

```text
feat: implement release and refund contract invocations
```

---

# Issue 10 — Configure Stellar RPC Client

## Description

Implement a reusable Stellar RPC client that will be shared across the relayer for transaction submission and network queries.

The client should centralize network communication and configuration.

## Requirements and Context

* Read RPC configuration from environment.
* Initialize Stellar RPC client.
* Export reusable client instance.
* Handle invalid configuration.
* Keep RPC logic isolated from business services.

This client will be used by both the Stellar Service and Transaction Status Service.

## Suggested Execution

```text
git checkout -b feat/stellar-rpc-client

Configure RPC client

Load configuration

Export reusable instance

Handle configuration errors

Add tests
```

## Example Commit Message

```text
feat: configure reusable Stellar RPC client
```


# Issue 11 — Implement Fee Bump Transaction Builder

## Description

Implement the Fee Bump transaction builder responsible for sponsoring transaction fees on behalf of users.

This is the core feature that enables the Web2.5 experience by allowing users to interact with Soroban contracts without holding XLM.

## Requirements and Context

* Accept an unsigned transaction XDR.
* Construct a Fee Bump transaction.
* Configure the sponsor account.
* Return the sponsored transaction.
* Keep sponsorship logic isolated from submission.

Do not submit the transaction in this issue.

## Suggested Execution

```text
git checkout -b feat/fee-bump-builder

Implement Fee Bump builder

Load sponsor account

Wrap unsigned transaction

Return sponsored transaction

Add unit tests
```

## Example Commit Message

```text
feat: implement Fee Bump transaction builder
```

---

# Issue 12 — Implement Transaction Signing

## Description

Implement the signing flow for sponsored transactions using the configured Fee Bump sponsor account.

The signing process should remain isolated from transaction construction and submission.

## Requirements and Context

* Read sponsor secret from configuration.
* Sign sponsored transactions.
* Return signed transaction.
* Handle invalid signing configuration.
* Never expose private keys through logs or API responses.

Signing should be reusable across future transaction types.

## Suggested Execution

```text
git checkout -b feat/transaction-signing

Load sponsor credentials

Sign sponsored transaction

Return signed transaction

Handle signing failures

Write unit tests
```

## Example Commit Message

```text
feat: implement sponsored transaction signing
```

---

# Issue 13 — Submit Transactions to Stellar RPC

## Description

Implement the transaction submission workflow responsible for broadcasting signed transactions to the Stellar network.

This issue completes the end-to-end transaction pipeline.

## Requirements and Context

* Accept signed transaction.
* Submit transaction to Stellar RPC.
* Capture submission response.
* Return transaction hash.
* Handle submission failures gracefully.

Submission logic should remain reusable for future contract actions.

## Suggested Execution

```text
git checkout -b feat/submit-transactions

Implement submission service

Submit signed transaction

Capture response

Return transaction hash

Add tests
```

## Example Commit Message

```text
feat: submit sponsored transactions to Stellar RPC
```

---

# Issue 14 — Normalize Transaction Submission Responses

## Description

Create a consistent response format for all transaction submissions.

Consumers of the relayer should receive predictable responses regardless of the underlying Stellar SDK response structure.

## Requirements and Context

Normalize successful responses to include:

* Success status
* Transaction hash
* Network
* Timestamp

Normalize failed responses to include:

* Success status
* Error code
* Error message

Avoid leaking raw SDK responses to clients.

## Suggested Execution

```text
git checkout -b feat/normalize-submission-response

Create response formatter

Normalize success responses

Normalize error responses

Update submission service

Write unit tests
```

## Example Commit Message

```text
feat: normalize Stellar transaction responses
```

---

# Issue 15 — Implement Transaction Status Lookup

## Description

Implement the transaction status service responsible for retrieving the current status of submitted transactions from the Stellar network.

This allows client applications to monitor transaction progress after submission.

## Requirements and Context

* Accept transaction hash.
* Query Stellar RPC.
* Return current transaction status.
* Handle unknown transaction hashes.
* Keep status lookup independent from transaction submission.

This service will power the transaction status endpoint exposed by the API.

## Suggested Execution

```text
git checkout -b feat/transaction-status

Implement transaction lookup

Query Stellar RPC

Return normalized status

Handle missing transactions

Add unit tests
```

## Example Commit Message

```text
feat: implement transaction status lookup
```


# Issue 16 — Parse Transaction Status Responses

## Description

Implement a response parser that converts raw Stellar RPC transaction status responses into a consistent format for client applications.

This abstraction keeps Stellar-specific response structures out of the API layer.

## Requirements and Context

* Parse successful transaction responses.
* Parse pending transaction responses.
* Parse failed transaction responses.
* Return a normalized response object.
* Keep parsing logic reusable and independent from HTTP routes.

The parser should become the single source of truth for interpreting transaction status responses.

## Suggested Execution

```text id="2v8bdb"
git checkout -b feat/status-response-parser

Create response parser

Normalize RPC responses

Handle different transaction states

Export reusable parser

Write unit tests
```

## Example Commit Message

```text id="0cmvsl"
feat: implement transaction status response parser
```

---

# Issue 17 — Handle Failed Transaction States

## Description

Improve the relayer's handling of failed Stellar transactions by mapping blockchain failures to consistent API responses.

This ensures clients receive meaningful error information without exposing internal SDK details.

## Requirements and Context

Handle scenarios including:

* Transaction rejected
* Contract execution failure
* Network failure
* Invalid transaction
* Unknown transaction

Return standardized error responses for each failure scenario.

## Suggested Execution

```text id="0em4tb"
git checkout -b feat/transaction-failure-handling

Map Stellar failures

Normalize error responses

Update status service

Improve logging

Write unit tests
```

## Example Commit Message

```text id="jlwmx5"
feat: improve transaction failure handling
```

---

# Issue 18 — Expand Unit Test Coverage

## Description

Increase unit test coverage across the relayer to ensure the MVP is reliable and maintainable.

Focus on testing service behavior rather than implementation details.

## Requirements and Context

Add tests covering:

* Environment configuration
* Request validation
* Transaction builder
* Fee Bump service
* Transaction signing
* Transaction submission
* Transaction status lookup
* Error handling

Tests should remain isolated and deterministic.

## Suggested Execution

```text id="34f7vh"
git checkout -b test/expand-unit-tests

Review existing coverage

Add missing tests

Refactor duplicated test setup

Verify all tests pass
```

## Example Commit Message

```text id="h8gq7l"
test: expand relayer unit test coverage
```

---

# Issue 19 — Configure Docker and Continuous Integration

## Description

Improve the developer experience by containerizing the relayer and automating quality checks through GitHub Actions.

This ensures contributors can validate changes consistently across environments.

## Requirements and Context

Configure:

* Dockerfile
* `.dockerignore`
* GitHub Actions workflow

CI should verify:

* Dependency installation
* Linting
* Unit tests

The workflow should run automatically on pull requests.

## Suggested Execution

```text id="53sq3r"
git checkout -b ci/docker-and-github-actions

Create Dockerfile

Configure GitHub Actions

Run linting

Run tests

Verify CI pipeline
```

## Example Commit Message

```text id="tq5b6y"
ci: add Docker support and GitHub Actions workflow
```

---

# Issue 20 — Improve API Documentation

## Description

Complete the v0.1.0 documentation by documenting the relayer's public API endpoints, expected request payloads, response formats, and common error responses.

Clear API documentation improves the onboarding experience for contributors and client applications.

## Requirements and Context

Document:

* Available endpoints
* Request bodies
* Success responses
* Error responses
* Environment requirements
* Example API calls

Ensure the documentation reflects the current MVP implementation.

## Suggested Execution

```text id="bt8pv6"
git checkout -b docs/api-documentation

Document API endpoints

Add request examples

Add response examples

Review documentation

Update README if needed
```

## Example Commit Message

```text id="jlwm2u"
docs: document relayer API for v0.1.0
```

