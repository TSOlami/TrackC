import { Table, Thead, Tbody, Tr, Th, Td, Center } from "@chakra-ui/react";

const TopCryptoTable = ({ cryptoData }) => {
  return (
    <Center>
      <Table variant="striped" colorScheme="gray">
        <Thead>
          <Tr>
            <Th>Crypto Name</Th>
            <Th>Symbol</Th>
            <Th>Slug</Th>
            <Th>Price</Th>
            <Th>Volume</Th>
            <Th>24hr</Th>
          </Tr>
        </Thead>
        <Tbody>
          {cryptoData.map((crypto) => (
            <Tr key={crypto.id}>
              <Td>{crypto.name}</Td>
              <Td>{crypto.symbol}</Td>
              <Td>{crypto.slug}</Td>
              <Td>{crypto.quote.USD.price}</Td>
              <Td>{crypto.quote.USD.volume_24h}</Td>
              <Td>{crypto.quote.USD.percent_change_24h}</Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Center>
  );
};

export default TopCryptoTable;
