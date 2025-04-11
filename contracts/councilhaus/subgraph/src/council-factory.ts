import { CouncilCreated as CouncilCreatedEvent } from "../generated/CouncilFactory/CouncilFactory";
import { Council } from "../generated/schema";
import { Council as CouncilTemplate } from "../generated/templates";
import { Council as CouncilContract } from "../generated/templates/Council/Council";

export function handleCouncilCreated(event: CouncilCreatedEvent): void {
  const councilAddress = event.params.council;
  const entity = new Council(event.params.council.toHex());

  const councilContract = CouncilContract.bind(councilAddress);

  entity.metadata = event.params.metadata;
  entity.pool = event.params.pool;
  entity.distributionToken = councilContract.distributionToken();
  entity.maxAllocationsPerMember = councilContract.maxAllocationsPerMember();
  entity.createdAt = event.block.timestamp;

  entity.save();

  CouncilTemplate.create(councilAddress);
}
