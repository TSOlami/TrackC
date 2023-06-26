import { useState } from 'react';
import { FormControl, FormLabel, Input, Button, Text } from '@chakra-ui/react';

const LoginForm = ({ handleLogin, loginError }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    handleLogin(e, formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <FormControl id="email">
        <FormLabel>Email</FormLabel>
        <Input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          autoComplete="email"
        />
      </FormControl>

      <FormControl id="password">
        <FormLabel>Password</FormLabel>
        <Input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          autoComplete="current-password"
        />
      </FormControl>

      {loginError && <Text color="red">{loginError}</Text>}

      <Button type="submit">Login</Button>

      <Text mt={4} color="gray.600">
        Demo Account Credentials:
        <br />
        Email: demo@gmail.com
        <br />
        Password: demo1234
      </Text>
    </form>
  );
};

export default LoginForm;
