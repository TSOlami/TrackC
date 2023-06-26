import { Box, Heading, Input, Button } from '@chakra-ui/react';

const LoginForm = ({ handleLogin }) => {
  return (
    <Box p={4}>
      <Heading as="h2" size="lg" mb={4}>
        Login
      </Heading>
      <form onSubmit={handleLogin}>
        <Input type="text" placeholder="Username" mb={2} />
        <Input type="password" placeholder="Password" mb={2} />
        <Button type="submit">Login</Button>
      </form>
      <Box mt={4}>
        <p>Use the following credentials for demo:</p>
        <p>Username: demo</p>
        <p>Password: demo123</p>
      </Box>
    </Box>
  );
};

export default LoginForm;