import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { useToast } from "@/components/ui/use-toast";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";

import { Input } from "@/components/ui/input";

import "./App.css";
import { Resource, Result, Unauthorized } from "./Projects";

("use client");


function WebsiteForm({ project_id, updateProject, setOpen }: { project_id: string, updateProject: () => void, setOpen: (open: boolean) => void }) {
  const { toast } = useToast();

  const websiteFormSchema = z.object({
    name: z.string(),
    url: z.string().url({ message: "Invalid URL" }),
  });


  const websiteForm = useForm<z.infer<typeof websiteFormSchema>>({
    mode: "onSubmit",
    resolver: zodResolver(websiteFormSchema),
    defaultValues: {
      name: "",
      url: "",
    },
  });


  async function onSubmitWebsiteForm(values: z.infer<typeof websiteFormSchema>) {
    console.log(values)
    const access_token = localStorage.getItem("accessToken");
    if (access_token) {
      const result = await createWebsiteResource(access_token, values.name, values.url, project_id);
      if (result.value) {
        toast({
          description: "Successfully created resource",
        });
        updateProject();
        setOpen(false);
      } else {
        toast({
          description: "There was an error creating resource. Please try again!",
        });
      }
    } else {
      window.location.assign(
        "http://localhost:5173/auth/login"
      );
    }
  }

  async function createWebsiteResource(access_token: string, name: string, url: string, project_id: string): Promise<Result<Resource, Error>> {
    try {
      const response = await fetch(`http://localhost:8081/resources/website`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${access_token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: name,
          url: url,
          project_id: project_id,
        })
      })
      if (response.ok) {
        const responseData = await response.json();
        return { value: responseData, error: null };
      } else {
        if (response.status === 401) {
          window.location.assign(
            "http://localhost:5173/auth/login"
          );
          return { value: null, error: new Unauthorized() }
        }
        return { value: null, error: Error(response.statusText) };
      }
    } catch (error) {
      return { value: null, error: Error(JSON.stringify(error)) };
    }
  }

  return (
    <Form {...websiteForm}>
      <form onSubmit={websiteForm.handleSubmit(onSubmitWebsiteForm)}>
        <div className="grid w-full items-center gap-4 pt-5">
          <div className="flex flex-col space-y-1.5">
            <FormField
              control={websiteForm.control}
              name="name"
              render={({ field, formState }) => (
                <FormItem>
                  <FormLabel className="font-extrabold pb-2">Name</FormLabel>
                  <FormControl>
                    <Input
                      {...field}
                      placeholder="Resource Name"
                      autoCapitalize="none"
                      autoComplete="true"
                      autoCorrect="off"
                      disabled={formState.isSubmitting}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={websiteForm.control}
              name="url"
              render={({ field, formState }) => (
                <FormItem className="pt-4">
                  <FormLabel className="font-extrabold pb-2">URL</FormLabel>
                  <FormControl>
                    <Input
                      {...field}
                      placeholder="Website URL"
                      autoCapitalize="none"
                      autoComplete="true"
                      autoCorrect="off"
                      disabled={formState.isSubmitting}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <div className="flex pt-3 pb-3">
              <Button className="justify-items-center">Create</Button>
            </div>
          </div>
        </div>
      </form>
    </Form>

  )

}

export default WebsiteForm;