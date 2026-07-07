# Issue #3 — feat: define storage keys for escrow persistence

## Description

Introduce the storage key definitions used to persist escrow data within Soroban storage.

These keys provide a stable interface for future storage operations.

---

## Requirements & Context

Create a `DataKey` enum covering all storage requirements for the MVP.

Structure the keys to support future contract expansion.

---

## Acceptance Criteria

* [ ] `DataKey` enum created.
* [ ] Naming follows project conventions.
* [ ] Compiles successfully.
* [ ] Documented.

---

## Out of Scope

* Reading storage
* Writing storage
* Escrow business logic

---

## Suggested Execution

```bash
git checkout -b feat/storage-keys
```

---

## Suggested Commit Message

```text
feat: define escrow storage keys
```

---

## Testing Notes

Compilation verification only.

---

## References

Issue #2

---

## Definition of Done

* [ ] Ready for review.




# Issue #4 — feat: implement storage helper utilities

## Description

Implement reusable helper functions for reading and writing escrow state to Soroban storage.

These helpers will centralize storage logic and reduce duplication across the contract.

---

## Requirements & Context

Implement helper methods for:

* Store escrow
* Retrieve escrow
* Update escrow

Helpers should return appropriate errors where necessary and avoid duplicated storage logic.

---

## Acceptance Criteria

* [ ] Storage helper module created.
* [ ] Read helper implemented.
* [ ] Write helper implemented.
* [ ] Update helper implemented.
* [ ] Unit tests added where applicable.
* [ ] Compiles successfully.

---

## Out of Scope

* Authentication
* Token transfers
* Events
* Escrow lifecycle logic

---

## Suggested Execution

```bash
git checkout -b feat/storage-helpers
```

---

## Suggested Commit Message

```text
feat: implement escrow storage helpers
```

---

## Testing Notes

Verify:

* Escrow can be stored.
* Escrow can be retrieved.
* Updated state persists correctly.

---

## References

Issues #2 and #3

---

## Definition of Done

* [ ] All acceptance criteria satisfied.
* [ ] Tests pass.
* [ ] Ready for maintainer review.



# Issue #5 — feat: implement create_escrow entrypoint

## Description

The contract currently has no mechanism for creating an escrow agreement. Implement the `create_escrow` entrypoint, which initializes a new escrow and persists it to contract storage.

This function is the starting point of every escrow lifecycle and should only be responsible for creating the escrow record—not locking funds or transferring tokens.

---

## Requirements & Context

Implement a `create_escrow()` function that:

* Accepts the buyer address.
* Accepts the seller address.
* Accepts the token contract address.
* Accepts the escrow amount.
* Creates an `EscrowState`.
* Sets the initial status to `Created`.
* Persists the escrow using the storage helpers.

---

## Acceptance Criteria

* [ ] `create_escrow()` implemented.
* [ ] Escrow is stored successfully.
* [ ] Initial status is `Created`.
* [ ] Function compiles.
* [ ] Unit tests added.

---

## Out of Scope

* Authentication
* Token transfers
* Events
* Refunds
* Release flow

---

## Suggested Execution

```bash
git checkout -b feat/create-escrow
```

---

## Suggested Commit Message

```text
feat: implement create_escrow entrypoint
```

---

## Testing Notes

Verify:

* Escrow is persisted.
* Fields are stored correctly.
* Initial status equals `Created`.

---

## References

* Issue #2
* Issue #4

---

## Definition of Done

* [ ] Acceptance criteria completed.
* [ ] Tests pass.
* [ ] Ready for review.

---

# Issue #6 — feat: require buyer authorization during escrow creation

## Description

Escrow creation should only be initiated by the buyer creating the agreement.

Implement buyer authorization using Soroban's `require_auth()` mechanism.

---

## Requirements & Context

Update `create_escrow()` so that:

* Buyer must authorize the transaction.
* Unauthorized callers are rejected.

Use Soroban authentication best practices.

---

## Acceptance Criteria

* [ ] Buyer authorization added.
* [ ] Unauthorized calls fail.
* [ ] Existing functionality continues to work.
* [ ] Tests added.

---

## Out of Scope

* Seller authorization
* Mediator permissions
* Token transfers

---

## Suggested Execution

```bash
git checkout -b feat/buyer-auth
```

---

## Suggested Commit Message

```text
feat: require buyer authorization
```

---

## Testing Notes

Verify:

* Buyer can create escrow.
* Unauthorized caller is rejected.

---

## References

Issue #5

---

## Definition of Done

* [ ] Tests pass.
* [ ] Ready for review.

---

# Issue #7 — feat: validate escrow creation input

## Description

Prevent invalid escrow records from being created by validating all required input before persisting state.

This protects the contract against malformed escrow agreements.

---

## Requirements & Context

Validate at minimum:

* Buyer address is valid.
* Seller address is valid.
* Buyer and seller are different.
* Amount is greater than zero.

Return appropriate contract errors.

---

## Acceptance Criteria

* [ ] Input validation implemented.
* [ ] Invalid requests rejected.
* [ ] Error handling follows project conventions.
* [ ] Tests added.

---

## Out of Scope

* Token balance validation
* Token transfers
* Escrow funding

---

## Suggested Execution

```bash
git checkout -b feat/create-escrow-validation
```

---

## Suggested Commit Message

```text
feat: validate escrow creation input
```

---

## Testing Notes

Verify:

* Zero amount rejected.
* Buyer == seller rejected.
* Valid request succeeds.

---

## References

Issue #5

---

## Definition of Done

* [ ] Acceptance criteria completed.
* [ ] Tests pass.
* [ ] Ready for review.

---

# Issue #8 — feat: add seller authorization for fund release

## Description

Escrow funds should only be released through authorized participants in the escrow lifecycle.

Implement seller-side authorization requirements where appropriate in preparation for the release flow.

This issue establishes the authorization foundation before token transfer logic is introduced.

---

## Requirements & Context

Implement reusable authorization logic for the seller.

The authorization should integrate cleanly with the upcoming `release_funds()` implementation.

---

## Acceptance Criteria

* [ ] Seller authorization helper implemented.
* [ ] Unauthorized access rejected.
* [ ] Tests added.
* [ ] Reusable by future contract functions.

---

## Out of Scope

* Release logic
* Token transfers
* Events
* Refunds

---

## Suggested Execution

```bash
git checkout -b feat/seller-auth
```

---

## Suggested Commit Message

```text
feat: implement seller authorization
```

---

## Testing Notes

Verify:

* Seller authorization succeeds.
* Unauthorized caller is rejected.

---

## References

* Issue #6
* Dependency Map

---

## Definition of Done

* [ ] Acceptance criteria completed.
* [ ] Tests pass.
* [ ] Ready for maintainer review.


# Issue #9 — feat: integrate Soroban Token Client

## Description

The escrow contract currently has no interaction with the Soroban Token Interface. Implement the token client integration that will be used throughout the escrow lifecycle to facilitate token transfers.

This serves as the foundation for all fund movement within the contract.

---

## Requirements & Context

* Import and instantiate the Soroban `token::Client`.
* Create reusable helper(s) for obtaining a token client from a token contract address.
* Keep the implementation reusable for future escrow operations.

---

## Acceptance Criteria

* [ ] Soroban Token Client integrated.
* [ ] Reusable helper(s) implemented.
* [ ] Code compiles successfully.
* [ ] Unit tests added where appropriate.

---

## Out of Scope

* Locking funds
* Releasing funds
* Refunding funds
* Events

---

## Suggested Execution

```bash
git checkout -b feat/token-client
```

---

## Suggested Commit Message

```text
feat: integrate Soroban Token Client
```

---

## Testing Notes

Verify:

* Token client initializes successfully.
* Helper methods are reusable by other contract functions.

---

## References

* Soroban Token Interface
* Issue #5

---

## Definition of Done

* [ ] Acceptance criteria completed.
* [ ] Ready for review.

---

# Issue #10 — feat: implement lock_funds

## Description

Implement the `lock_funds()` entrypoint.

This function transfers funds from the buyer into the escrow and updates the escrow status to `Locked`.

This is the first point where assets are actually secured by the contract.

---

## Requirements & Context

Implement `lock_funds()` so that it:

* Requires buyer authorization.
* Retrieves the escrow.
* Uses the stored token address.
* Transfers funds into escrow.
* Updates escrow status to `Locked`.
* Persists the updated escrow.

---

## Acceptance Criteria

* [ ] Buyer authorization enforced.
* [ ] Funds transferred into escrow.
* [ ] Escrow status updated.
* [ ] Storage updated.
* [ ] Tests added.

---

## Out of Scope

* Release flow
* Refund flow
* Events

---

## Suggested Execution

```bash
git checkout -b feat/lock-funds
```

---

## Suggested Commit Message

```text
feat: implement lock_funds
```

---

## Testing Notes

Verify:

* Buyer can successfully lock funds.
* Escrow status becomes `Locked`.
* Storage reflects the updated state.

---

## References

* Issue #5
* Issue #9

---

## Definition of Done

* [ ] Acceptance criteria completed.
* [ ] Tests pass.
* [ ] Ready for review.

---

# Issue #11 — feat: implement release_funds

## Description

Implement the `release_funds()` entrypoint.

This function completes the escrow by transferring funds from the escrow to the seller.

It represents the successful completion of the escrow lifecycle.

---

## Requirements & Context

Implement `release_funds()` so that it:

* Validates escrow state.
* Uses the stored token address.
* Transfers funds to the seller.
* Updates escrow status to `Released`.
* Persists the updated escrow.

---

## Acceptance Criteria

* [ ] Funds transferred successfully.
* [ ] Escrow status updated to `Released`.
* [ ] Invalid state transitions rejected.
* [ ] Storage updated.
* [ ] Tests added.

---

## Out of Scope

* Refund flow
* Events
* Human Oracle integration

---

## Suggested Execution

```bash
git checkout -b feat/release-funds
```

---

## Suggested Commit Message

```text
feat: implement release_funds
```

---

## Testing Notes

Verify:

* Funds reach the seller.
* Escrow status becomes `Released`.
* Releasing an already released escrow fails.

---

## References

* Issue #8
* Issue #10

---

## Definition of Done

* [ ] Acceptance criteria completed.
* [ ] Tests pass.
* [ ] Ready for review.

---

# Issue #12 — feat: implement refund flow

## Description

Implement the `refund()` entrypoint to allow escrow funds to be returned to the buyer before the escrow has been completed.

This provides the second valid completion path for the MVP.

---

## Requirements & Context

Implement `refund()` so that it:

* Validates escrow state.
* Transfers escrowed funds back to the buyer.
* Updates escrow status to `Refunded`.
* Persists the updated escrow.

---

## Acceptance Criteria

* [ ] Refund transfers funds successfully.
* [ ] Escrow status becomes `Refunded`.
* [ ] Invalid refunds rejected.
* [ ] Storage updated.
* [ ] Tests added.

---

## Out of Scope

* Human mediator approval
* Dispute resolution
* Events

---

## Suggested Execution

```bash
git checkout -b feat/refund-flow
```

---

## Suggested Commit Message

```text
feat: implement refund flow
```

---

## Testing Notes

Verify:

* Buyer receives refunded funds.
* Escrow status becomes `Refunded`.
* Released escrows cannot be refunded.

---

## References

* Issue #10
* v0.1.0 MVP Scope

---

## Definition of Done

* [ ] Acceptance criteria completed.
* [ ] Tests pass.
* [ ] Ready for maintainer review.



# Issue #13 — feat: validate escrow state transitions

## Description

The contract should only allow valid escrow state transitions. Implement centralized validation logic to prevent illegal transitions throughout the escrow lifecycle.

This improves contract safety and keeps lifecycle rules consistent across all entrypoints.

---

## Requirements & Context

Implement reusable validation logic enforcing:

* `Created → Locked`
* `Locked → Released`
* `Locked → Refunded`

Reject all other transitions.

---

## Acceptance Criteria

* [ ] State transition validator implemented.
* [ ] Invalid transitions return appropriate contract errors.
* [ ] Existing functions use the validator.
* [ ] Unit tests added.

---

## Out of Scope

* Human Oracle
* Timeouts
* Disputes
* Events

---

## Suggested Execution

```bash
git checkout -b feat/state-transition-validation
```

---

## Suggested Commit Message

```text
feat: validate escrow state transitions
```

---

## Testing Notes

Verify:

* Valid transitions succeed.
* Invalid transitions fail.
* Released escrows cannot change state.

---

## References

* Issues #10–#12

---

## Definition of Done

* [ ] Acceptance criteria completed.
* [ ] Tests pass.
* [ ] Ready for review.

---

# Issue #14 — feat: prevent duplicate escrow funding

## Description

Once an escrow has been funded, additional calls to `lock_funds()` should be rejected.

This prevents accidental or malicious double funding.

---

## Requirements & Context

Update `lock_funds()` to reject escrows that are already in the `Locked`, `Released`, or `Refunded` states.

Return an appropriate contract error.

---

## Acceptance Criteria

* [ ] Duplicate funding prevented.
* [ ] Existing happy path unaffected.
* [ ] Unit tests added.

---

## Out of Scope

* Refund flow
* Release flow
* Events

---

## Suggested Execution

```bash
git checkout -b feat/prevent-double-funding
```

---

## Suggested Commit Message

```text
feat: prevent duplicate escrow funding
```

---

## Testing Notes

Verify:

* First funding succeeds.
* Second funding fails.
* Escrow state remains unchanged.

---

## References

* Issue #10
* Issue #13

---

## Definition of Done

* [ ] Acceptance criteria completed.
* [ ] Tests pass.

---

# Issue #15 — feat: introduce contract error enum

## Description

The contract currently lacks a centralized error model.

Introduce a contract-wide `Error` enum to standardize failures across the escrow lifecycle.

---

## Requirements & Context

Create explicit error variants for scenarios such as:

* Unauthorized
* InvalidState
* EscrowNotFound
* InvalidAmount
* EscrowAlreadyFunded

Ensure future errors can be added without breaking existing code.

---

## Acceptance Criteria

* [ ] Error enum created.
* [ ] Existing functions updated.
* [ ] Error handling standardized.
* [ ] Unit tests updated.

---

## Out of Scope

* New contract features
* Human Oracle errors

---

## Suggested Execution

```bash
git checkout -b feat/contract-errors
```

---

## Suggested Commit Message

```text
feat: introduce contract error enum
```

---

## Testing Notes

Verify:

* Errors are returned correctly.
* Existing tests continue to pass.

---

## References

* CONTRIBUTING.md

---

## Definition of Done

* [ ] Acceptance criteria completed.
* [ ] Tests pass.

---

# Issue #16 — refactor: extract reusable escrow validation helpers

## Description

Several entrypoints now perform similar validation logic.

Extract reusable validation helpers to reduce duplication and improve maintainability.

This refactor should not change contract behavior.

---

## Requirements & Context

Extract reusable helper functions for validating:

* Escrow existence
* Escrow ownership
* Escrow status
* Escrow mutability

Refactor existing functions to use these helpers.

---

## Acceptance Criteria

* [ ] Duplicate validation removed.
* [ ] Helper module created.
* [ ] Existing behavior unchanged.
* [ ] Tests continue to pass.

---

## Out of Scope

* New features
* Storage changes
* Token transfer changes

---

## Suggested Execution

```bash
git checkout -b refactor/validation-helpers
```

---

## Suggested Commit Message

```text
refactor: extract escrow validation helpers
```

---

## Testing Notes

Run the full test suite to ensure no regressions have been introduced.

---

## References

* Issues #5–#15

---

## Definition of Done

* [ ] Acceptance criteria completed.
* [ ] Full test suite passes.
* [ ] Ready for maintainer review.


# Issue #17 — feat: publish escrow lifecycle events

## Description

Implement event publishing for all major escrow lifecycle actions. Events allow off-chain services, explorers, and future indexers to observe contract activity without reading contract storage directly.

---

## Requirements & Context

Publish events for:

* EscrowCreated
* FundsLocked
* FundsReleased
* EscrowRefunded

Use consistent event topics and payloads.

---

## Acceptance Criteria

* [ ] Events emitted for escrow creation.
* [ ] Events emitted when funds are locked.
* [ ] Events emitted when funds are released.
* [ ] Events emitted when refunds occur.
* [ ] Existing tests updated.

---

## Out of Scope

* Event indexing
* Analytics
* Oracle events

---

## Suggested Execution

```bash
git checkout -b feat/escrow-events
```

---

## Suggested Commit Message

```text
feat: publish escrow lifecycle events
```

---

## Testing Notes

Verify each successful contract action emits the expected event.

---

## References

* Soroban Events Documentation
* Issues #5–#12

---

## Definition of Done

* [ ] Acceptance criteria completed.
* [ ] Tests pass.
* [ ] Ready for review.

---

# Issue #18 — test: implement comprehensive escrow lifecycle tests

## Description

The current test suite is scaffolded. Implement comprehensive tests covering the complete happy path of the escrow lifecycle.

---

## Requirements & Context

Add tests for:

* Escrow creation
* Locking funds
* Releasing funds
* Refunding funds

Verify storage and state transitions after every operation.

---

## Acceptance Criteria

* [ ] Happy path tests added.
* [ ] Storage assertions added.
* [ ] State transition assertions added.
* [ ] Tests pass consistently.

---

## Out of Scope

* Oracle testing
* Benchmarking

---

## Suggested Execution

```bash
git checkout -b test/escrow-lifecycle
```

---

## Suggested Commit Message

```text
test: add escrow lifecycle integration tests
```

---

## Testing Notes

Run the full suite using:

```bash
cargo test
```

---

## References

Issues #5–#17

---

## Definition of Done

* [ ] All lifecycle tests pass.
* [ ] Ready for review.

---

# Issue #19 — test: add authorization and failure-path tests

## Description

Ensure authorization checks and invalid contract operations behave correctly.

Every public contract function should reject unauthorized callers and invalid state transitions.

---

## Requirements & Context

Cover scenarios including:

* Unauthorized escrow creation
* Unauthorized release
* Duplicate funding
* Invalid refunds
* Invalid state transitions

---

## Acceptance Criteria

* [ ] Authorization tests added.
* [ ] Failure-path tests added.
* [ ] Error assertions included.

---

## Out of Scope

* Performance testing
* Fuzz testing

---

## Suggested Execution

```bash
git checkout -b test/auth-and-errors
```

---

## Suggested Commit Message

```text
test: add authorization and failure-path tests
```

---

## Testing Notes

Ensure every error condition introduced in previous issues is covered.

---

## References

Issues #6–#16

---

## Definition of Done

* [ ] Acceptance criteria completed.
* [ ] Tests pass.

---

# Issue #20 — refactor: improve test utilities and reduce duplication

## Description

As the test suite grows, duplicate setup logic becomes difficult to maintain.

Extract reusable helpers to simplify future test development.

---

## Requirements & Context

Refactor common setup into reusable utilities, including:

* Mock environment setup
* Test addresses
* Mock token creation
* Shared assertions

---

## Acceptance Criteria

* [ ] Duplicate setup removed.
* [ ] Helper functions introduced.
* [ ] Existing tests remain unchanged.
* [ ] Full test suite passes.

---

## Out of Scope

* New contract functionality

---

## Suggested Execution

```bash
git checkout -b refactor/test-helpers
```

---

## Suggested Commit Message

```text
refactor: extract reusable testing utilities
```

---

## Testing Notes

Run the complete test suite to verify no regressions.

---

## References

Issue #18

---

## Definition of Done

* [ ] Acceptance criteria completed.
* [ ] Ready for maintainer review.



# Batch 6 — Documentation, CI & Testnet Deployment

---

# Issue #21 — docs: improve repository README

## Description

The current README should evolve from a scaffold overview into contributor-focused documentation that explains the purpose of the project, the escrow lifecycle, local development workflow, and current MVP scope.

This will serve as the primary entry point for new contributors.

---

## Requirements & Context

Update the README to include:

* Project overview
* Escrow lifecycle diagram
* Architecture overview
* Local development instructions
* Testing instructions
* Current MVP scope
* Roadmap summary
* Related repositories

---

## Acceptance Criteria

* [ ] README updated.
* [ ] Development instructions verified.
* [ ] Architecture section added.
* [ ] Roadmap included.
* [ ] Links verified.

---

## Out of Scope

* API documentation
* SDK documentation

---

## Suggested Execution

```bash id="fb80hi"
git checkout -b docs/readme-refresh
```

---

## Suggested Commit Message

```text id="yuw9hy"
docs: improve repository README
```

---

## Testing Notes

Verify every documented command executes successfully.

---

## References

* CONTRIBUTING.md
* PadiPay Architecture

---

## Definition of Done

* [ ] Documentation reviewed.
* [ ] Ready for merge.

---

# Issue #22 — ci: add GitHub Actions workflow

## Description

Automate basic quality checks for every pull request.

Every contribution should automatically run formatting, linting, and tests before review.

---

## Requirements & Context

Create a GitHub Actions workflow that runs:

* cargo fmt --check
* cargo clippy
* cargo test

The workflow should execute for:

* Pull Requests
* Pushes to `main`

---

## Acceptance Criteria

* [ ] Workflow created.
* [ ] Formatting verified.
* [ ] Clippy verified.
* [ ] Tests executed automatically.

---

## Out of Scope

* Deployment automation
* Release automation

---

## Suggested Execution

```bash id="2u7h1d"
git checkout -b ci/github-actions
```

---

## Suggested Commit Message

```text id="g1qlkt"
ci: add GitHub Actions workflow
```

---

## Testing Notes

Open a test PR and verify the workflow completes successfully.

---

## References

GitHub Actions Documentation

---

## Definition of Done

* [ ] CI passes successfully.
* [ ] Ready for review.

---

# Issue #23 — chore: deploy contract to Stellar Testnet

## Description

Deploy the MVP contract to Stellar Testnet and document the deployment details.

This demonstrates that the contract is not only functional locally but also deployable to a live blockchain environment.

---

## Requirements & Context

Deploy the latest v0.1.0 contract to Stellar Testnet and document:

* Contract ID
* Network
* Deployment command
* Required environment variables

Update the repository with deployment instructions.

---

## Acceptance Criteria

* [ ] Contract successfully deployed.
* [ ] Contract ID documented.
* [ ] Deployment guide added.
* [ ] Deployment verified.

---

## Out of Scope

* Mainnet deployment
* Upgrade strategy

---

## Suggested Execution

```bash id="s2w5hs"
git checkout -b chore/testnet-deployment
```

---

## Suggested Commit Message

```text id="6jlwmr"
chore: deploy contract to Stellar Testnet
```

---

## Testing Notes

Verify deployed contract is callable using the documented contract ID.

---

## References

* Stellar CLI Documentation

---

## Definition of Done

* [ ] Deployment verified.
* [ ] Documentation updated.

---

# Issue #24 — docs: publish v0.1.0 release notes and roadmap

## Description

Prepare the repository for the first public milestone by documenting what has been delivered in v0.1.0 and what contributors can work on next.

This issue serves as the bridge between the MVP and future community development.

---

## Requirements & Context

Create release notes that include:

* Features delivered
* Known limitations
* Intentionally deferred features
* Future milestones
* Contributor opportunities

Create or update a `ROADMAP.md` summarizing:

* v0.2.0 — Contract Hardening
* v0.3.0 — Human Oracle Integration
* v0.4.0 — Production Readiness

---

## Acceptance Criteria

* [ ] Release notes written.
* [ ] ROADMAP.md updated.
* [ ] Deferred features documented.
* [ ] Future milestones documented.

---

## Out of Scope

* Code changes
* Contract upgrades

---

## Suggested Execution

```bash id="mt8vnr"
git checkout -b docs/v0.1-roadmap
```

---

## Suggested Commit Message

```text id="d1uvm0"
docs: publish v0.1.0 roadmap and release notes
```

---

## Testing Notes

Review documentation for consistency with the implemented MVP.

---

## References

* v0.1.0 MVP Scope
* Dependency Map

---

## Definition of Done

* [ ] Documentation reviewed.
* [ ] Ready for merge.



