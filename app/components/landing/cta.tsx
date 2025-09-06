import Link from 'next/link'
import { ArrowRight } from 'lucide-react'

export function CTA() {
  return (
    <section className="py-20 bg-primary-600">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
          Ready to get started?
        </h2>
        <p className="text-xl text-primary-100 mb-8 max-w-3xl mx-auto">
          Join thousands of patients and doctors who are already using our platform 
          to make healthcare more accessible and convenient.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            href="/auth/register"
            className="btn bg-white text-primary-600 hover:bg-gray-100 btn-lg inline-flex items-center"
          >
            Sign Up Free
            <ArrowRight className="ml-2 h-5 w-5" />
          </Link>
          <Link
            href="/doctors"
            className="btn border-2 border-white text-white hover:bg-white hover:text-primary-600 btn-lg"
          >
            Browse Doctors
          </Link>
        </div>
      </div>
    </section>
  )
}
