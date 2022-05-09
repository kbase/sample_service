# Debugging

References:

- reusable workflows


- event schema

Most of the properties utilized are derived from "github.event", an object provided in the context of a workflow triggered by a given event.

Some event properties are specific to a given event, others are common across most if not all events.

For instance `github.event.repository` is common across all the workflows we use and should be universal across all workflows:



- github object