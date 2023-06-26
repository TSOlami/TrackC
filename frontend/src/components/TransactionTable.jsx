import { Table, Thead, Tbody, Tr, Th, Td } from '@chakra-ui/react';

const TransactionTable = ({ transactions }) => {
  return (
    <Table variant="striped" colorScheme="gray">
      <Thead>
        <Tr>
          <Th>Date</Th>
          <Th>Type</Th>
          <Th>Amount</Th>
        </Tr>
      </Thead>
      <Tbody>
        {transactions.map((transaction) => (
          <Tr key={transaction.id}>
            <Td>{transaction.date}</Td>
            <Td>{transaction.type}</Td>
            <Td>{transaction.amount}</Td>
          </Tr>
        ))}
      </Tbody>
    </Table>
  );
};

export default TransactionTable;