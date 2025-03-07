# -*- coding: utf-8 -*-
"""frontend_app

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Jug-5K8qClHHDWvdocdYOM3DAjoYo21K
"""

import { useState } from "react";
import { Button, Input, Textarea } from "@/components/ui";
import { Card, CardContent } from "@/components/ui/card";

export default function AIPrototypingTool() {
  const [requirement, setRequirement] = useState("");
  const [screens, setScreens] = useState([]);

  const generateScreens = async () => {
    const response = await fetch("https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateText", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer YOUR_GEMINI_API_KEY`,
      },
      body: JSON.stringify({
        prompt: `Generate a structured UI screen list for the following app requirement:

        ${requirement}

        Format:
        - Screen Name
        - Short description`,
        max_tokens: 300,
      }),
    });

    const data = await response.json();
    const generatedText = data.candidates?.[0]?.output || "";

    const screens = generatedText.split("\n\n").map((screenText) => {
      const [name, description] = screenText.split("\n");
      return { name: name || "Unnamed Screen", description: description || "No description available." };
    });

    setScreens(screens);
  };

  const updateScreen = (index, field, value) => {
    const updatedScreens = [...screens];
    updatedScreens[index][field] = value;
    setScreens(updatedScreens);
  };

  return (
    <div className="grid grid-cols-2 gap-4 p-4 h-screen">
      <div className="flex flex-col gap-4">
        <h2 className="text-xl font-bold">Enter Product Requirement</h2>
        <Textarea
          value={requirement}
          onChange={(e) => setRequirement(e.target.value)}
          placeholder="Describe the app you want to build..."
          className="h-40"
        />
        <Button onClick={generateScreens}>Generate Screens</Button>
      </div>
      <div className="flex flex-col gap-4">
        <h2 className="text-xl font-bold">Generated Screens</h2>
        <div className="grid grid-cols-2 gap-4">
          {screens.map((screen, index) => (
            <Card key={index}>
              <CardContent>
                <Input
                  value={screen.name}
                  onChange={(e) => updateScreen(index, "name", e.target.value)}
                  className="text-lg font-semibold"
                />
                <Textarea
                  value={screen.description}
                  onChange={(e) => updateScreen(index, "description", e.target.value)}
                  className="mt-2"
                />
                <div className="mt-4 p-4 border rounded bg-gray-100">
                  <h3 className="font-bold">{screen.name}</h3>
                  <p>{screen.description}</p>
                  <Button className="mt-2">Example Button</Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}