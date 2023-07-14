from pydantic import BaseModel, Field


class PostSchema(BaseModel):
    title: str = Field(...)
    text: str = Field(...)
    user_id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "title": "Office Ipsum",
                "text": "What is lorem ipsum? why is the text in spanish? can we barter services?, but try a more "
                "powerful colour. Why is a 15mb gif on the startpage a bad idea?! it looks a bit empty, "
                "try to make everything bigger, for I think we need to start from scratch, but that's great, "
                "but we need to add this 2000 line essay. I'll know it when i see it this looks perfect. Just "
                "Photoshop out the dog, add a baby, and make the curtains blue, but can the black be darker, "
                "and I think we need to start from scratch, for could you do an actual logo instead of a font "
                "I have printed it out, but the animated gif is not moving, nor i cant pay you . Im not sure, "
                "try something else can we have another option can you make it faster? we don't need a "
                "backup, it never goes down!, nor i think this should be fairly easy so if you just want to "
                "have a look theres all this spanish text on my site, or can you turn it around in photoshop "
                "so we can see more of the front. Start on it today and we will talk about what i want next "
                "time can you make it pop, mmm, exactly like that, but different the hair is just too "
                "polarising, or I really think this could go viral. Make it look like Apple use a kpop logo "
                "that's not a kpop logo! ugh, nor we don't need a contract, do we, and we exceed the clients' "
                "expectations, and can you make it look more designed , so can you help me out? you will get "
                "a lot of free exposure doing this. Jazz it up a little we are a startup I need a website. "
                "How much will it cost can you help me out? you will get a lot of free exposure doing this, "
                "so what is a hamburger menu. Make it look like Apple. Could you rotate the picture to show "
                "the other side of the room? thats not what i saw in my head at all. Can you put 'find us on "
                "facebook' by the facebook logo? I have an awesome idea for a startup, i need you to build it "
                "for me. Concept is bang on, but can we look at a better execution that's great, but we need "
                "to add this 2000 line essay, nor can you make pink a little more pinkish I really think this "
                "could go viral, or we need to make the new version clean and sexy. Can the black be darker I "
                "have an awesome idea for a startup, i need you to build it for me can you make the logo "
                "bigger yes bigger bigger still the logo is too big mmm, exactly like that, but different can "
                "you punch up the fun level on these icons, and I like it, but can the snow look a little "
                "warmer. Is this the best we can do can't you just take a picture from the internet? could "
                "you move it a tad to the left we need to make the new version clean and sexy we are a "
                "non-profit organization.",
                "user_id": "1",
            }
        }
