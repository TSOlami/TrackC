import { Box, Heading } from '@chakra-ui/react';

const Profile = ({ username, portfolioWorth }) => {
  return (
    <Box p={4} bg="gray.200" borderRadius="md">
      <Heading as="h2" size="lg" mb={2}>
        Profile
      </Heading>
      <p>Username: {username}</p>
      <p>Net Worth: ${portfolioWorth}</p>
    </Box>
  );
};

export default Profile;