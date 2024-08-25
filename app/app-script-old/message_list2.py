message_dict = {
    'Comparing Dimensions' : {
        'opening': "In this activity, we will focus on reasoning about a mathematical situation.",
        'question': "The dimensions of four rectangles are given in the figure. Which rectangle looks most like a square? Explain your thinking using complete sentences.",
        "Expectation1": {
            "Expectation":"The closer a ratio of the sides in a rectangle is to one, the more it looks like a square.",
            "Hint1":"What is the relationship between the length and width of a square?  How could you use this information to determine if a rectangle looks more or less like a square?",
            "Hint2": [
                "Using the calculator, please compute the ratio of width to length for each rectangle. Think through what these ratios indicate about the rectangle ...", 
                "openPopupCalculator()", 
                "Now, you have computed the ratio for each rectangle as follows: 7/10 = 0.7, 17/20 = 0.85, 27/30 = 0.9, and 37/40 = 0.925. What do you notice about the ratio of each rectangle and how much they look like a square? "
            ]
            },
        "Expectation2": {
            "Expectation":"The larger the sides of the rectangle with a 3-unit difference, the more it looks like a square.",
            "Hint1":[
                "In the pop-up activity, you will see a rectangle with a 3-unit difference between the length and width. By dragging the corners, you can change the size of the rectangle, but there will still be a 3-unit difference in the length and width. Take a moment to manipulate the rectangle. As you make the dimensions larger and smaller, think about how the same 3-unit difference between length and width affects how much the rectangle does or does not look like a square.", 
                "openPopupDragboard()", 
                "As the length and width get bigger or smaller, how does the 3-unit difference between length and width impact the ratio of the dimensions?"
            ],
            "Hint2":[ 
                "openNewImage(./static/images/Rectangle2.png)", 
                "Let's only focus on the rectangles shown in the figure. Which of the two rectangles is most like a square and why?", 
                "Looking at the image and thinking about your answer to the previous question, would a 3-unit difference between the dimensions of an even larger rectangle look more or less like a square than a 3-unit different between the dimensions of a smaller rectangle? Explain your answer using complete sentences."
            ]
            },
        "Expectation3":{
            "Expectation":"The correct answer is the rectangle with dimensions 37 ft by 40 ft.",
            "Hint1":[
                "openNewImage(./static/images/Rectangle1.png)", 
                "Given the dimensions of the four rectangles, which rectangle do you think looks most like a square?"
            ],
            "Hint2":[
                "openNewImage(./static/images/Rectangle1.png)",
                "Which rectangle has a ratio of width to length that is closest to 1?"
            ]
            },
        "Conclusion":[
            "openNewImage(./static/images/Summary-ComparingDimensions.png)",
            "The ratio of length to width of a square is 1, and rectangles that have a ratio of length to width closer to 1 will look more like a square. We purposely selected these four rectangles to show how rectangles with the same 3-unit difference between length and width can have different ratios that cause the rectangle to look more or less like a square. As the dimensions get larger(i.e., 37x40), the effect of the 3-unit difference is less on the ratio and it will look more like a square. However, as the dimensions get smaller (i.e., 7x10), the effect of the 3-unit difference is greater on the ratio and it will look less like a square. It’s important to note here that because, the quotient of width and length (i.e., the ratio) and not the <i>difference</i> between the length and width determines how much a rectangle can look like a square."
            ]
    }, 

    "Making Iced Tea": {
        "opening": "In this activity, we will compare ratios.", 
        "question": "The red and blue pitchers in the figure contain sweetened iced tea that tastes the same and is a combination of liquid and sugar. One scoop of sugar is added to the red pitcher and one scoop of sugar is added to the blue pitcher. Compare the sweetness of the iced tea for each pitcher after adding one scoop of sugar. Explain your answer.",
        "Expectation1": {
            "Expectation":"Adding one scoop of sugar increases the ratio of sugar to liquid in the blue pitcher.",
            "Hint1":[
            "Let's assume there are 30 grams of sugar and 3 liters of liquid in the red pitcher and there are 10 grams of sugar and 1 liter of liquid in the blue pitcher. If 10 grams of sugar were added to both pitchers, please compute the new ratio of sugar to liquid for each pitcher using the calculator. When you are done, click the dismiss.",
            "openPopupCalculator()",
            "Now, you have computed the new ratio of sugar to liquid for each pitcher, 40/3 for the red pitcher and 20/1 for the blue pitcher. What can you say about the new ratios of sugar to liquid for the blue pitcher compared to the red pitcher?"
            ],
            "Hint2":[
            "After adding one scoop of sugar to each pitcher, which pitcher has a greater ratio of sugar to liquid? Remember to use complete sentences.",
            "openNewImage(./static/images/IcedTeah-MainBackground.jpg)"
            ]
            },
        "Expectation2":{
            "Expectation":"The blue pitcher is affected more because it has less liquid.",
            "Hint1":"Recall that the red and blue pitchers originally had the same taste of sweetness, which means that the quantity of sugar per a given amount of liquid was the same in each pitcher. How does adding the same amount of sugar to different amounts of liquid affect the taste of sweetness for each pitcher?",
            "Hint2":"Remember that taste of sweetness is dependent on the amount of sugar per unit of liquid. After adding the same amount of sugar, why would the taste of sweetness for the blue pitcher be affected more than the taste of sweetness for the red pitcher?"
        },
        "Expectation3":{
            "Expectation":"The blue pitcher tastes sweeter.",
            "Hint1":"Recall that the red and blue pitchers originally had the same taste of sweetness. After adding one scoop of sugar, which pitcher would taste sweeter?",
            "Hint2":"After adding one scoop of sugar, which pitcher would have a greater ratio of sugar to liquid?"},
        "Conclusion":[
            "The amount of sugar per unit of liquid determines the sweetness of the iced tea. Although both pitchers originally had the same taste of sweetness, adding one scoop of sugar will increase the amount of sugar per unit of liquid in the blue pitcher than in the red pitcher. This is because the blue pitcher contains less liquid than the red pitcher. As you see in this activity, the taste of sweetness is determined by the amount of sugar per unit of liquid.",
            "openNewImage(./static/images/Summary-MakingIcedTea.jpg)"
            ]
    },

    "Mixing Paint":{
        'opening':"In this activity, we will explore relationships among two quantities in three different mixtures.", 
        "question": "Sarah is painting her room gray by mixing green and red paints, where more green paint in the mixture produces a darker shade of gray.    <br><br>    She starts by making Mixture A, using 4 parts green paint with 3 parts red paint. She ran out of Mixture A before finishing her room and decided to make more of the same shade of gray paint.  So, Sarah makes Mixture B, using 5 parts green paint and 4 parts red paint, adding one more part of each paint to produce a larger batch.  Realizing she still isn’t finished after using all of Mixture B, Sarah makes a final batch of gray paint to finish painting her room.  In Mixture C, she uses 6 parts green paint and 5 parts red paint, adding one more part of each pant to make an even larger batch.    <br>    <ul>    <li>Mixture A had 4 parts of green paint and 3 of parts red paint.</li>    <li>Mixture B had 5 parts of green paint and 4 parts of red paint.</li>    <li>Mixture C had 6 parts of green paint and 5 parts of red paint.</li>    </ul>   <br>    Looking at her fully painted room, arah realizes that the walls painted by these mixtures are three different shades!  Why did Sarah’s mixtures all produce different shades of gray and which of the mixtures is the darkest shade?",
        "Expectation1":{
            "Expectation":"The shade of gray for each mixture is dependent on the number of green parts per red part.",
            "Hint1":[
            "openNewImage(./static/images/Screen_Shot_2020-11-11_at_1.24.43_PM.png)",
            "In each mixture the green and red paints are mixed homogeneously. For each mixture, consider how many parts of green paint there are per one part of red paint. What does this tell us about why the shades of gray are different?"
            ],
            "Hint2":[
            "openNewImage(./static/images/Screen_Shot_2020-11-11_at_1.24.43_PM.png)",
            "Consider the different shades produced by Mixtures A, B, and C.  What determines the shade of gray?"
            ]
        },
        "Expectation2":{
            "Expectation":"The constant difference will not keep the shade the same because there is a multiplicative relationship between the green and red paint in each mixture.",
            "Hint1":[
            "openNewImage(./static/images/Screen_Shot_2020-11-11_at_1.24.43_PM.png)",
            "Sarah created Mixture B and C by adding the same amount of green and red paints to the previous mixture; but, they resulted in different shades of gray.  Why does adding the same amount of green and red paint to the previous mixture not make the same shade of gray?"
            ],
            "Hint2":[
            "openNewImage(./static/images/Screen_Shot_2020-11-11_at_1.24.43_PM.png)",
            "Adding the same amount of green and red paint did not produce the same shade of gray. This indicates that the same shade cannot be created by keeping the difference between the green and red parts constant. What about the mixture of green and red paint needs to be constant to produce larger batches of the same shade of gray?" 
            ]
        },
        "Expectation3":{
            "Expectation":"Mixture A is the darkest shade of gray.",
            "Hint1":[
            "openNewImage(./static/images/Screen_Shot_2020-11-11_at_1.21.18_PM.png)",
            "In each mixture, the green and red paint are mixed homogeneously and more green paint in the mixture produces a darker shade of gray. For each mixture, compute how many parts of green paint are needed for every one part of red paint.",
            "openPopupCalculator()", 
            "Use this information to decide which mixture is the darkest shade of gray."
            ],
            "Hint2":[
            "openNewImage(./static/images/Screen_Shot_2020-11-11_at_1.21.18_PM.png)",
            "The mixture with the most parts of green paint for every one part of red paint will produce the darkest shade of gray. Which mixture has the most parts green paint per one part red paint?"
            ]
        },
        "Conclusion":[
            "openNewImage(./static/images/Screen_Shot_2020-11-11_at_1.26.21_PM.png)",
            "When working on problems like this, students often think that adding or subtracting the same amount to each quantity will produce the same results. This is because students often think keeping the difference between variable quantities constant will keep the relationship between the quantities the same. In contrast, as we see in this activity, the shade of gray is dependent on the amount of a quantity per one unit of the other quantity (i.e., green parts per one part red).  This means when the quotient of the two quantities is constant, the mixture will produce the same shade of gray. It’s important for students to understand that some relationships depend on the constant quotient of the quantities to produce the same outcomes, rather than the constant difference between the quantities."
        ]
    }
}