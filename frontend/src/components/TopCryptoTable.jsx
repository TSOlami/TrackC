import { Table, Thead, Tbody, Tr, Th, Td } from '@chakra-ui/react';

const TopCryptoTable = ({ cryptoData }) => {
  return (
    <Table variant="striped" colorScheme="gray">
      <Thead>
        <Tr>
          <Th>Crypto Currency</Th>
          <Th>Price</Th>
        </Tr>
      </Thead>
      <Tbody>
        {cryptoData.map((crypto) => (
          <Tr key={crypto.id}>
            <Td>{crypto.currency}</Td>
            <Td>{crypto.price}</Td>
          </Tr>
        ))}
      </Tbody>
    </Table>
  );
};

export default TopCryptoTable;