import { BigInt } from "@graphprotocol/graph-ts";
import { log, store } from "@graphprotocol/graph-ts";
import {
  Allocation,
  Council,
  CouncilMember,
  Grantee,
  CouncilManager,
  Vote,
} from "../generated/schema";
import {
  RoleGranted,
  RoleRevoked,
  BudgetAllocated,
  CouncilMemberAdded,
  CouncilMemberRemoved,
  CouncilMemberEdited,
  GranteeAdded,
  GranteeRemoved,
  MaxAllocationsPerMemberSet,
} from "../generated/templates/Council/Council";

export function handleRoleGranted(event: RoleGranted): void {
  const councilManager = new CouncilManager(
    `${event.address.toHex()}-${event.params.role.toHex()}-${event.params.account.toHex()}`,
  );
  const council = Council.load(event.address.toHex());

  if (!council) {
    log.warning("Council not found for role {} and account {}", [
      event.params.role.toHex(),
      event.params.account.toHex(),
    ]);

    return;
  }

  councilManager.account = event.params.account;
  councilManager.role = event.params.role;
  councilManager.council = council.id;
  councilManager.createdAt = event.block.timestamp;

  councilManager.save();
}

export function handleRoleRevoked(event: RoleRevoked): void {
  const id = `${event.address.toHex()}-${event.params.role.toHex()}-${event.params.account.toHex()}`;

  store.remove("CouncilManager", id);
}

export function handleCouncilMemberAdded(event: CouncilMemberAdded): void {
  const councilMember = new CouncilMember(
    `${event.address.toHex()}-${event.params.member.toHex()}`,
  );
  councilMember.account = event.params.member;
  councilMember.votingPower = event.params.votingPower;
  councilMember.council = event.address.toHex();

  councilMember.save();
}

export function handleCouncilMemberRemoved(event: CouncilMemberRemoved): void {
  const councilMemberId = `${event.address.toHex()}-${event.params.member.toHex()}`;

  store.remove("CouncilMember", councilMemberId);
}

export function handleCouncilMemberEdited(event: CouncilMemberEdited): void {
  const councilMemberId = `${event.address.toHex()}-${event.params.member.toHex()}`;
  const councilMember = CouncilMember.load(councilMemberId);

  if (!councilMember) {
    log.warning("Council member not found for id {}", [councilMemberId]);

    return;
  }

  councilMember.votingPower = event.params.votingPower;

  councilMember.save();
}

export function handleGranteeAdded(event: GranteeAdded): void {
  const grantee = new Grantee(
    `${event.address.toHex()}-${event.params.grantee.toHex()}`,
  );
  grantee.metadata = event.params.metadata;
  grantee.account = event.params.grantee;
  grantee.council = event.address.toHex();

  grantee.save();
}

export function handleGranteeRemoved(event: GranteeRemoved): void {
  const granteeId = `${event.address.toHex()}-${event.params.grantee.toHex()}`;

  store.remove("Grantee", granteeId);
}

export function handleBudgetAllocated(event: BudgetAllocated): void {
  const allocation = new Allocation(
    `${event.transaction.hash.toHex()}-${event.logIndex.toString()}`,
  );
  const councilMember = CouncilMember.load(
    `${event.address.toHex()}-${event.params.member.toHex()}`,
  );

  if (!councilMember) {
    log.warning("Council member not found, skipping allocation", [
      event.params.member.toHex(),
    ]);
    return;
  }

  allocation.council = event.address.toHex();
  allocation.councilMember = councilMember.id;
  allocation.allocatedAt = event.block.timestamp;

  const amounts = event.params.allocation.amounts;
  const accounts = event.params.allocation.accounts;
  const votes: string[] = [];

  for (let i = 0; i < accounts.length; i++) {
    const grantee = Grantee.load(
      `${event.address.toHex()}-${accounts[i].toHex()}`,
    );

    if (!grantee) {
      log.warning("Not all grantees found, skipping allocation", [
        accounts[i].toHex(),
      ]);
      return;
    }

    const vote = new Vote(
      `${event.params.member.toHex()}-${grantee.account}-${
        event.block.timestamp
      }`,
    );

    vote.grantee = grantee.id;
    vote.amount = amounts[i];

    vote.save();
    votes.push(vote.id);
  }

  allocation.votes = votes;
  allocation.save();
}

export function handleMaxAllocationsPerMemberSet(
  event: MaxAllocationsPerMemberSet,
): void {
  const council = Council.load(event.address.toHex());

  if (council) {
    council.maxAllocationsPerMember = event.params.maxAllocationsPerMember;
    council.save();
  }
}
