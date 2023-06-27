import { Box, Flex, Heading, Spacer } from '@chakra-ui/react';
import LogoutButton from './LogoutButton';

const Header = () => {
  return (
    <Box bg="blue.500" p={4} color="white">
      <Flex>
        <Heading as="h1" size="lg">
          TrackC
        </Heading>
        <Spacer />
        {/* Logout button */}
        <LogoutButton />
      </Flex>
    </Box>
  );
};

export default Header;
