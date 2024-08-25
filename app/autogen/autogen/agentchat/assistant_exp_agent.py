from typing import Callable, Dict, Literal, Optional, Union

from .conversable_writable_agent import ConversableWritableAgent


class AssistantExpAgent(ConversableWritableAgent):
    """(In preview) Assistant agent, designed to solve a task with LLM.

    AssistantAgent is a subclass of ConversableWritableAgent configured with a default system message.
    The default system message is designed to solve a task with LLM,
    including suggesting python code blocks and debugging.
    `human_input_mode` is default to "NEVER"
    and `code_execution_config` is default to False.
    This agent doesn't execute code by default, and expects the user to execute the code.
    """

    DEFAULT_SYSTEM_MESSAGE = """
        You are a Judger (Judge Assistant). Decide which expected points of a mathematical solution are explicitly and correctly covered by the user response. 
        # Input Data 
        ## (1) [Question]: one math question; 
        ## (2) [Expectations]: consist of several [Expectation]; each [Expectation] is one reasoning or final answer to the [Question]; 
        ## (3) [Response]: users' responses, indicated by {\"speaker\":\"USER\"}; 
        ## (4) [CoversationHistory](optional): conversation history of two parts, 
        ### (4-1) prior user responses, indicated by {\"speaker\":\"USER\"}; 
        ### (4-2) system hint, indicated by {\"speaker\":\"AGENT\"} helping the user cover more expectations.
        # Workflow 
        ## 1. With the given [Question] and [Expectations], split the expectations with assigned order number \"1,2,3...\" to each [Expectation]; 
        ## 2. Contrastive Comparison: find the focus and subject of each [Expectation] compared with others;
        ## 3. Check: With the [Response] of user, including in [ConversationHistory] and the current [Response], check which [Expectation] are explicitly covered and the reasoning paths are correctly followed.
        ## Revise: you may get the reply from another judge assistant like you, but with different viewpoints. When it is this case, please consider his or her reply and decide if to accept and revise, or persist on your original judgement, and then reply again. No matter if you agree with other Judge assistant, you must reply with the full output again. Exclude the output dictionary, the explanation should be no longer than 200 words.
        # Instruction
        ## Solve the task step by step if you need to. If a [Response] is ambiguous, compare the potential [Expectation] first, and then check if the [Response] covers each [Expectation] independently.
        ## Decide on final [Response]. Your reply is merely based on the final [Response]. The [CoversationHistory] only provides the context information, and does not serve as evidence of your judgement.
        ## Supportive information. When user [Response] is vague or conveys limited information, or user is answering to system questions or hints, you can turn to the questions or hints from system in the last speech, and make judgement based on both the question/hint and [Response].
        ## Self-consistency. Your judgement is based on user [Response]. If any [Expectation] is covered by the information provided by system, do not include it in your reply.
        ## When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible.
        # Output Format: ## Reply a dictionary, with keys"evidence" and "output" ## "evidence" is the verifiable evidence, no longer than 50 words for each [Expectation] if any. ## "output" is a list of integer numbers that indicate the order number(s) of covered [Expectation]}; ## Examples of "output": [1], [2,3], or [1,2,3]. ## If no expectation is covered, just set "output" as []. ## Do not reply with explanations or judgement out of the dictionary.
    """

    DEFAULT_DESCRIPTION = "A helpful and general-purpose AI assistant that has strong language skills, mathematical and pedagogical knowldege."

    def __init__(
        self,
        name: str,
        system_message: Optional[str] = DEFAULT_SYSTEM_MESSAGE,
        llm_config: Optional[Union[Dict, Literal[False]]] = None,
        is_termination_msg: Optional[Callable[[Dict], bool]] = None,
        max_consecutive_auto_reply: Optional[int] = None,
        human_input_mode: Optional[str] = "NEVER",
        code_execution_config: Optional[Union[Dict, Literal[False]]] = False,
        description: Optional[str] = None,
        **kwargs,
    ):
        """
        Args:
            name (str): agent name.
            system_message (str): system message for the ChatCompletion inference.
                Please override this attribute if you want to reprogram the agent.
            llm_config (dict): llm inference configuration.
                Please refer to [OpenAIWrapper.create](/docs/reference/oai/client#create)
                for available options.
            is_termination_msg (function): a function that takes a message in the form of a dictionary
                and returns a boolean value indicating if this received message is a termination message.
                The dict can contain the following keys: "content", "role", "name", "function_call".
            max_consecutive_auto_reply (int): the maximum number of consecutive auto replies.
                default to None (no limit provided, class attribute MAX_CONSECUTIVE_AUTO_REPLY will be used as the limit in this case).
                The limit only plays a role when human_input_mode is not "ALWAYS".
            **kwargs (dict): Please refer to other kwargs in
                [ConversableWritableAgent](conversable_agent#__init__).
        """
        super().__init__(
            name,
            system_message,
            is_termination_msg,
            max_consecutive_auto_reply,
            human_input_mode,
            code_execution_config=code_execution_config,
            llm_config=llm_config,
            description=description,
            **kwargs,
        )

        # Update the provided description if None, and we are using the default system_message,
        # then use the default description.
        if description is None:
            if system_message == self.DEFAULT_SYSTEM_MESSAGE:
                self.description = self.DEFAULT_DESCRIPTION
