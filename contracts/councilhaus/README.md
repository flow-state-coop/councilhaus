# Flow Council

In order to deploy the contracts, follow the steps below:

 ```shell
 npx hardhat vars set ALCHEMY_KEY # API key from Alchemy.com
 npx hardhat vars set WALLET_KEY # Private key of the wallet that will deploy the contracts
 bun run deploy:<network>
 ```

In order to verify the contracts, follow the steps below:
 
 ```shell
 npx hardhat vars set ETHERSCAN_KEY_OPTIMISM # API key from optimistic.etherscan.io
 # or
 npx hardhat vars set ETHERSCAN_KEY_BASE # API key from basescan.org
 
 npx hardhat verify --network <network> <factoryAddress> 0x6DA13Bde224A05a288748d857b9e7DDEffd1dE08
 npx hardhat verify --network <network> <councilAddress> "Spacing Guild" "SPA" <distributionTokenAddress> 0x6DA13Bde224A05a288748d857b9e7DDEffd1dE08
 ```
 
 In order to deploy the subgraph, follow the steps below:
 
 ```shell
 cd subgraph
 bun install
 nano config/<network>.json # set the correct block number
 bun build:<network>
 bun deploy:<network>
 ```

## Contract Deployments

### Arbitrum

<table>
<thead>
    <tr>
        <th>Contract</th>
        <th>Address</th>
    </tr>
</thead>
<tbody>
    <tr>
        <td>Council Factory</td>
        <td>0xe6a6E24905e200F69b57cE3B01D5F65776a40DF3</td>
    </tr>
</tbody>
</table>

### Base

<table>
<thead>
    <tr>
        <th>Contract</th>
        <th>Address</th>
    </tr>
</thead>
<tbody>
    <tr>
        <td>Council Factory</td>
        <td>0x73DD388BC769eD4975Cb4e6Cfd9a5b9474082875</td>
    </tr>
</tbody>
</table>

### Celo

<table>
<thead>
    <tr>
        <th>Contract</th>
        <th>Address</th>
    </tr>
</thead>
<tbody>
    <tr>
        <td>Council Factory</td>
        <td>0x25B64C200cf3362BaC6961353D38A1dbEB42e60E</td>
    </tr>
</tbody>
</table>


### Optimism

<table>
<thead>
    <tr>
        <th>Contract</th>
        <th>Address</th>
    </tr>
</thead>
<tbody>
    <tr>
        <td>Council Factory</td>
        <td>0xeba33Eb3B2aa36EC81390b4e10b4f61b555f194b</td>
    </tr>
</tbody>
</table>

### Optimism Sepolia

<table>
<thead>
    <tr>
        <th>Contract</th>
        <th>Address</th>
    </tr>
</thead>
<tbody>
    <tr>
        <td>Council Factory</td>
        <td>0x0037c884f51714fEA8194E3C0c547894736bF8F2</td>
    </tr>
</tbody>
</table>
