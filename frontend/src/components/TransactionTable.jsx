import { Table, Thead, Tbody, Tr, Th, Td } from "@chakra-ui/react";

const TransactionTable = ({ transactions }) => {
  return (
    <Table variant="striped" colorScheme="gray">
      <Thead>
        <Tr>
          <Th>Coin Name</Th>
          <Th>Amount</Th>
          <Th>Symbol</Th>
          <Th>Price Purchased At</Th>
          <Th>No. of Coins</Th>
          <Th>Time Transacted</Th>
          <Th>Time Updated</Th>
        </Tr>
      </Thead>
      <Tbody>
        {transactions.map((transaction) => (
          <Tr key={transaction.time_updated}>
            <Td>{transaction.coin_name}</Td>
            <Td>{transaction.amount}</Td>
            <Td>{transaction.symbol}</Td>
            <Td>{transaction.price_purchased_at}</Td>
            <Td>{transaction.no_of_coins}</Td>
            <Td>{transaction.time_transacted}</Td>
            <Td>{transaction.time_updated}</Td>
          </Tr>
        ))}
      </Tbody>
    </Table>
  );
};

export default TransactionTable;
