import { Star } from 'lucide-react'

const testimonials = [
  {
    name: 'Sarah Johnson',
    role: 'Patient',
    content: 'The video consultation was so convenient. I could see my doctor from home and got my prescription the same day.',
    rating: 5,
  },
  {
    name: 'Dr. Michael Chen',
    role: 'Cardiologist',
    content: 'This platform has made it so much easier to connect with patients and provide quality care remotely.',
    rating: 5,
  },
  {
    name: 'Emily Rodriguez',
    role: 'Patient',
    content: 'The appointment booking system is intuitive and the reminders help me stay on top of my health.',
    rating: 5,
  },
]

export function Testimonials() {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            What our users say
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Don't just take our word for it. Here's what patients and doctors 
            are saying about our platform.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <div key={index} className="card p-6">
              <div className="flex items-center mb-4">
                {[...Array(testimonial.rating)].map((_, i) => (
                  <Star key={i} className="h-5 w-5 text-yellow-400 fill-current" />
                ))}
              </div>
              <p className="text-gray-600 mb-4 italic">
                "{testimonial.content}"
              </p>
              <div>
                <div className="font-semibold text-gray-900">
                  {testimonial.name}
                </div>
                <div className="text-sm text-gray-500">
                  {testimonial.role}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
