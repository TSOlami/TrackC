import { useState } from 'react';
import { Box, Heading, Flex, Spacer, Link } from '@chakra-ui/react';
import { NavLink } from 'react-router-dom';

const HomePage = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  const handleToggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <Box>
      <Flex bg="teal.500" py={4} px={6} color="white" alignItems="center">
        <Box>
          <Link as={NavLink} to="/" fontSize="lg" fontWeight="semibold">
            My App
          </Link>
        </Box>
        <Spacer />
        <Box>
          <Link as={NavLink} to="/login" mr={4}>
            Login
          </Link>
          <Link as={NavLink} to="/signup">
            Sign Up
          </Link>
        </Box>
      </Flex>

      <Flex>
        {isSidebarOpen && (
          <Box
            bg="gray.800"
            w="200px"
            color="white"
            p={4}
            position="fixed"
            left={0}
            top={0}
            bottom={0}
          >
            <Box mb={4}>
              <Link as={NavLink} to="/home" fontSize="lg" fontWeight="bold" color="teal.500">
                Home/Dashboard
              </Link>
            </Box>
            <Box mb={4}>
              <Link as={NavLink} to="/profile" fontSize="lg" fontWeight="bold">
                Profile
              </Link>
            </Box>
            <Box mb={4}>
              <Link as={NavLink} to="/about" fontSize="lg" fontWeight="bold">
                About Us
              </Link>
            </Box>
            <Box mb={4}>
              <Link as={NavLink} to="/support" fontSize="lg" fontWeight="bold">
                Support/Feedback
              </Link>
            </Box>
            <Box mb={4}>
              <Link as={NavLink} to="/logout" fontSize="lg" fontWeight="bold">
                Logout
              </Link>
            </Box>
          </Box>
        )}

        <Box p={4} ml={isSidebarOpen ? '200px' : 0} transition="margin-left 0.3s ease">
          <Heading as="h1" size="xl" mb={4}>
            Home Page
          </Heading>
          <h1>Welcome to the Home Page</h1>
          <button
            onClick={handleToggleSidebar}
            className="absolute top-4 left-4 bg-gray-800 text-white px-2 py-1 rounded"
          >
            {isSidebarOpen ? 'Close Sidebar' : 'Open Sidebar'}
          </button>
        </Box>
      </Flex>
    </Box>
  );
};

export default HomePage;
