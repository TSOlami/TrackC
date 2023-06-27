import { Box, Heading } from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import SignupForm from "../components/SignupForm";

const SignupPage = () => {
  const navigate = useNavigate();

  return (
    <Box p={4}>
      <Heading as="h1" size="xl" mb={4}>
        Sign Up Page
      </Heading>
      <SignupForm navigate={navigate} />
    </Box>
  );
};

export default SignupPage;
