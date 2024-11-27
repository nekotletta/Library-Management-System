import React, { useState, ChangeEvent, FormEvent } from 'react';

import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Label } from './ui/label';

export default function LoginForm() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleEmailChange = (event: ChangeEvent<HTMLInputElement>) => {
        setEmail(event.target.value);
    };

    const handlePasswordChange = (event: ChangeEvent<HTMLInputElement>) => {
        setPassword(event.target.value);
    };

    const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
      event.preventDefault();
  
      const url = 'http://100.127.68.1:8005'; // Replace with your Django API endpoint
      const data = {
          email: email,
          password: password,
      };
  
      try {
          const response = await fetch(url, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',   
  
              },
              body: JSON.stringify(data),
          });
  
          if (!response.ok) {
              throw new Error(`Error: ${response.statusText}`);
          }
  
          const responseData = await response.json();
          console.log(responseData);   
  
          // Handle response data as needed
      } catch (error) {
          console.error('Error:', error);
      }
  };

    return (
        <div className="flex h-screen w-full items-center justify-center bg-gray-100 px-4">
            <Card className="w-full max-w-sm">
                <CardHeader>
                    <CardTitle className="text-2xl">Login</CardTitle>
                    <CardDescription>
                        Enter your email below to login to your account
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <form className="grid gap-4" onSubmit={handleSubmit}>
                        <div className="grid gap-2">
                            <Label htmlFor="email">Email</Label>
                            <Input
                                id="email"
                                type="email"
                                placeholder="m@example.com"
                                required
                                value={email}
                                onChange={handleEmailChange}
                            />
                        </div>
                        <div className="grid gap-2">
                            <div className="flex items-center justify-between">
                                <Label htmlFor="password">Password</Label>
                                <a href="#" className="text-sm text-blue-500 hover:text-blue-600">
                                    Forgot password?
                                </a>
                            </div>
                            <Input
                                id="password"
                                type="password"
                                required
                                value={password}
                                onChange={handlePasswordChange}
                            />
                        </div>
                        <Button type="submit" className="w-full">
                            Login
                        </Button>
                    </form>
                    <div className="mt-4 text-center text-sm">
                        Don't have an account?{' '}
                        <a href="#" className="text-blue-500 hover:text-blue-600">
                            Sign up
                        </a>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}