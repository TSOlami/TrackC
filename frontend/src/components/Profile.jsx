import { Box, Heading } from '@chakra-ui/react';

const Profile = ({ name, portfolioWorth }) => {
  return (
    <Box p={4} bg="gray.200" borderRadius="md">
      <Heading as="h2" size="lg" mb={2}>
        Profile
      </Heading>
      <p>Name: {name}</p>
      <p>Portfolio Worth: {portfolioWorth}</p>
    </Box>
  );
};

export default Profile;